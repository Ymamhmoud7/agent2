import ollama
import re
import os
import json

from utils import ollama_utils
from prompts import PLANNER_PROMPT

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

def execute_plan(plan: dict, executor) -> list[str]:
    results = []


    def resolve_args(args: dict, i: int = 0) -> dict:
        resolved = {}
        for k, v in args.items():
            if isinstance(v, str):
                v = os.path.expanduser(v)
                def replace_expr(match):
                    expr = match.group(1).strip()
                    try:
                        return str(eval(expr, {"i": i}))
                    except:
                        return match.group(0) 
                v = re.sub(r'\{([^}]+)\}', replace_expr, v)
            resolved[k] = v
        return resolved
    
    def run_steps(steps: list, i: int = 0):
        for step in steps:
            if step["type"] == "call":
                args = resolve_args(step.get("args", {}), i)
                result = executor(step["function"], args)
                results.append(f"[call] {step['function']}({args}) → {result}")
            elif step['type'] == 'loop':
                count = step.get("count", 0)
                body = step.get("body", [])
                for idx in range(count):
                    run_steps(body, i=idx)
    
    run_steps(plan.get("plan", []))
    return results