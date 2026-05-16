import ollama
import re
import os
import json

from utils import ollama_utils
from prompts import PLANNER_PROMPT

def _expand_comprehension(expr: str) -> str:
    count_match = re.search(r'range\((\d+)\)', expr)
    template_match = re.search(r'\{(.*?)\}(?=\s*for)', expr, re.DOTALL)
    if not count_match or not template_match:
        return expr
    count = int(count_match.group(1))
    template = '{' + template_match.group(1) + '}'
    template = re.sub(r'f"(.*?)"', r'"\1"', template)
    template = re.sub(r"f'(.*?)'", r'"\1"', template)
    items = [template] * count
    return '[' + ','.join(items) + ']'

def sanitize_raw(raw: str) -> str:
    raw = re.sub(r'\bTrue\b', 'true', raw)
    raw = re.sub(r'\bFalse\b', 'false', raw)
    raw = re.sub(r'\bNone\b', 'null', raw)
    raw = re.sub(r'f"(.*?)"', r'"\1"', raw)
    raw = re.sub(r"f'(.*?)'", r'"\1"', raw)
    raw = re.sub(r'\[\s*\{.*?\}\s*for\s+\w+\s+in\s+range\(\d+\)\s*\]',
                 lambda m: _expand_comprehension(m.group(0)), raw, flags=re.DOTALL)
    return raw

def plan_actions(user_input: str, skills_context: str, model: str, retries: int = 3):
    if not ollama_utils.ollama_status():
        ollama_utils.ollama_serve()

    prompt = f"""Available skills and functions:
{skills_context}

User request: {user_input}

Produce the JSON execution plan:"""

    for attempt in range(retries):
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": PLANNER_PROMPT.PLANNER_PROMPT},
                {"role": "user", "content": prompt},
            ],
            options={"temperature": 0.0, "num_predict": 512},
        )

        raw = response["message"]["content"].strip()
        raw = sanitize_raw(raw)
        # Strip markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        print(f"[planner raw attempt {attempt+1}]:\n{raw}\n")  # debug

        try:
            parsed = json.loads(raw)
            return {"plan": parsed.get("plan", [])}
        except json.JSONDecodeError as e:
            print(f"[planner] JSON parse failed (attempt {attempt+1}): {e}")

    return {"plan": [], "error": "Failed to parse valid JSON after retries."}

def reflect_on_results(user_input: str, results: list[str], model: str) -> str:
    results_str = "\n".join(results)

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a task assistant reporting execution results to the user. "
                    "You will be given the original request and the results of each action as Python dicts. "
                    "Rules for interpreting results: "
                    "'success: True' means the action worked regardless of other field values. "
                    "'connected: False' means the VPN is OFF, it is NOT a failure. "
                    "'connected: True' means the VPN is ON. "
                    "Report clearly what happened in plain English. "
                    "Only call something a failure if 'success' is False. "
                    "Be concise, 1-3 sentences max."
                )
            },
            {
                "role": "user",
                "content": f"Original request: {user_input}\n\nExecution results:\n{results_str}"
            }
        ],
        options={"temperature": 0.3, "num_predict": 256}
    )

    return response["message"]["content"].strip()

def execute_plan(plan: dict, executor) -> list[str]:
    results = []
    context = {}  

    def resolve_args(args: dict, i: int = 0) -> dict:
        resolved = {}
        for k, v in args.items():
            if isinstance(v, str):
                v = os.path.expanduser(v)
                def replace_expr(match):
                    expr = match.group(1).strip()
                    try:
                        return str(eval(expr, {"i": i, **context}))
                    except:
                        return match.group(0)
                v = re.sub(r'\{([^}]+)\}', replace_expr, v)
            resolved[k] = v
        return resolved

    def run_steps(steps: list, i: int = 0):
        for step in steps:
            stype = step.get("type")

            if stype in ("call", "query"):
                args = resolve_args(step.get("args", {}), i)
                result = executor(step["function"], args)
                label = "query" if stype == "query" else "call"
                results.append(f"[{label}] {step['function']}({args}) → {result}")

                # store result in context if requested
                store_as = step.get("store_as")
                if store_as and isinstance(result, dict):
                    context[store_as] = result

            elif stype == "loop":
                for idx in range(step.get("count", 0)):
                    run_steps(step.get("body", []), i=idx)

            elif stype == "conditional":
                condition = step.get("condition", "")
                condition = condition.replace("true", "True").replace("false", "False").replace("null", "None")
                try:
                    outcome = bool(eval(condition, {"__builtins__": {}}, context))
                except Exception as e:
                    results.append(f"[conditional] failed to evaluate '{condition}': {e}")
                    continue

                branch = step.get("if_true", []) if outcome else step.get("if_false", [])
                run_steps(branch, i)

    run_steps(plan.get("plan", []))
    return results