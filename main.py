import curses
import router

from utils import send_message
from cli import ChatUI


def handle_ai_message(message, ui):
    """Route message and stream AI response tokens into the UI."""

    eval = router.eval_user_input(message, "qwen2.5:3b")
    if eval == "Action":
        ui.print("Action detected!", ui.colour(3))

    elif eval == "Not Action":
        
        
        token_gen = send_message.message(message, "qwen2.5:3b")

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

    else:
        ui.print(f"Unknown message type: {eval1}", ui.colour(3))


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