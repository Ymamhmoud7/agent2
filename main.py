import curses
import router
import json

from utils import send_message, get_skills, read_skill, planner, executor
from cli import ChatUI
from skills import create_folder

def build_skills_context():
    skills = get_skills.get_skills()

    if not skills:
        return "No skills available."

    lines = ["Available skills and functions:"]
    for skill_name in skills:
        skill_info = read_skill.read_skill(skill_name)
        lines.append(f"\nSkill: {skill_name}")
        if skill_info["functions"]:
            for func in skill_info["functions"]:
                desc = f" — {func['description']}" if func['description'] else ""
                lines.append(f"  - {func['name']}{desc}")
        else:
            lines.append("  (no functions found)")

        examples = skill_info.get("examples", [])
        if examples:
            lines.append("  Examples:")
            for ex in examples:
                lines.append(f'    User: "{ex["user"]}"')
                lines.append(f'    Plan: {json.dumps(ex["plan"])}')

    return "\n".join(lines)

def handle_ai_message(message, ui):
    """Route message and stream AI response tokens into the UI."""

    eval = router.eval_user_input(message, "qwen2.5:3b")
    ui.print(f"Routing to {eval} evaluation...", ui.colour(4))
    if eval == "action":
        skills_context = build_skills_context()
        plan = planner.plan_actions(
            message,
            skills_context,
            model="qwen2.5:3b"
        )

        if "error" in plan:
            ui.print(f"Planning error: {plan['error']}", ui.colour(1))
            return
        
        if not plan.get("plan"):
            ui.print("No actions found for that request.", ui.colour(3))
            return

        results = planner.execute_plan(plan, executor.executor)
        reflection = planner.reflect_on_results(message, results, model="qwen2.5:3b")
        ui.print("", ui.colour(4))
        ui.print(reflection, ui.colour(1))
    else:
        token_gen = send_message.message(message, (eval == "simple" and "qwen2.5:3b") or "qwen3.5:4b")

        current_line = ""
        for token in token_gen:
            for char in token:
                if char == "\n":
                    ui.flush_line(current_line)
                    current_line = ""
                else:
                    current_line += char
                    ui.print_token(char, len(current_line) - 1)

        if current_line:
            ui.flush_line(current_line)

def run(stdscr):
    curses.curs_set(1)
    stdscr.clear()

    ui = ChatUI(stdscr)

    ui.print("Chat started. Type /exit to quit, /clear to clear output.", ui.colour(3))
    ui.print("")
    ui.refresh_input()

    input_buf = []

    while True:
        ui.refresh_input("".join(input_buf))
        ch = ui.get_char()
        code = ord(ch) if isinstance(ch, str) else ch

        # Enter
        if code in (10, 13, curses.KEY_ENTER):
            message = "".join(input_buf).strip()
            input_buf.clear()

            if not message:
                continue

            ui.print(f"> {message}", ui.colour(2) | ui.BOLD)

            if message == "/exit":
                ui.print("Bye!", ui.colour(3))
                curses.napms(800)
                break

            if message == "/clear":
                ui.clear_output()
                continue

            handle_ai_message(message, ui)
            ui.print("")

        # Backspace
        elif code in (8, 127, curses.KEY_BACKSPACE):
            if input_buf:
                input_buf.pop()

        # Scroll
        elif code == curses.KEY_UP:
            ui.scroll_up()
        elif code == curses.KEY_DOWN:
            ui.scroll_down()

        # Printable characters
        elif isinstance(ch, str) and ch.isprintable():
            input_buf.append(ch)
        elif code >= 32:
            input_buf.append(chr(code))


if __name__ == "__main__":
    curses.wrapper(run)