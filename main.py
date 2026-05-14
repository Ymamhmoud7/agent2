import curses
import router

from utils import send_message


def draw_border(win, title=None):
    """Draw a single-line border using = chars on top and bottom."""
    h, w = win.getmaxyx()
    border_line = "=" * w
    try:
        win.addstr(0, 0, border_line)
        win.addstr(h - 1, 0, border_line[: w - 1]) 
    except curses.error:
        pass
    if title:
        win.addstr(0, 2, f" {title} ")


def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)     # borders
    curses.init_pair(2, curses.COLOR_GREEN, -1)    # prompt
    curses.init_pair(3, curses.COLOR_YELLOW, -1)   # system messages
    curses.init_pair(4, curses.COLOR_WHITE, -1)    # normal output

    max_h, max_w = stdscr.getmaxyx()

    # Layout:
    #  ┌─────────────────────┐
    #  │  output area        │  (most of the screen)
    #  ├─────────────────────┤
    #  │ =================== │  top border of input box
    #  │ > (INPUT)           │  input line
    #  │ =================== │  bottom border of input box
    #  └─────────────────────┘
    INPUT_BOX_HEIGHT = 3   # top border + input line + bottom border
    OUTPUT_HEIGHT = max_h - INPUT_BOX_HEIGHT

    # Output scroll pad (tall virtual area)
    PAD_HEIGHT = 1000
    out_pad = curses.newpad(PAD_HEIGHT, max_w)
    out_pad.scrollok(True)

    # Input window (3 rows: border, input, border)
    in_win = curses.newwin(INPUT_BOX_HEIGHT, max_w, OUTPUT_HEIGHT, 0)

    # Track pad scroll position
    pad_scroll = 0
    pad_line = 0  # next line to write in pad

    def pad_print(text, attr=curses.A_NORMAL):
        nonlocal pad_line
        # Word-wrap manually if needed
        for chunk in [text[i:i+max_w-1] for i in range(0, max(len(text), 1), max_w-1)]:
            try:
                out_pad.addstr(pad_line, 0, chunk, attr)
            except curses.error:
                pass
            pad_line += 1
        # Auto-scroll to bottom
        nonlocal pad_scroll
        visible_lines = OUTPUT_HEIGHT - 1
        if pad_line > visible_lines:
            pad_scroll = pad_line - visible_lines
        out_pad.refresh(pad_scroll, 0, 0, 0, OUTPUT_HEIGHT - 1, max_w - 1)

    def refresh_input(current_text=""):
        in_win.clear()
        h, w = in_win.getmaxyx()
        border = "=" * w
        try:
            in_win.addstr(0, 0, border, curses.color_pair(1))
            in_win.addstr(2, 0, border[: w - 1], curses.color_pair(1))
        except curses.error:
            pass
        prompt = "> "
        in_win.addstr(1, 0, prompt, curses.color_pair(2) | curses.A_BOLD)
        in_win.addstr(1, len(prompt), current_text, curses.color_pair(4))
        in_win.move(1, len(prompt) + len(current_text))
        in_win.refresh()

    # Welcome message
    pad_print("Chat started. Type /exit to quit, /clear to clear output.", curses.color_pair(3))
    pad_print("")

    refresh_input()

    input_buf = []

    while True:
        refresh_input("".join(input_buf))
        ch = in_win.get_wch()

        if isinstance(ch, str):
            code = ord(ch)
        else:
            code = ch

        # Enter
        if code in (10, 13, curses.KEY_ENTER):
            message = "".join(input_buf).strip()
            input_buf.clear()

            if not message:
                refresh_input()
                continue

            # Echo user input
            pad_print(f"> {message}", curses.color_pair(2) | curses.A_BOLD)

            if message == "/exit":
                pad_print("Bye!", curses.color_pair(3))
                out_pad.refresh(pad_scroll, 0, 0, 0, OUTPUT_HEIGHT - 1, max_w - 1)
                curses.napms(800)
                break

            if message == "/clear":
                out_pad.clear()
                pad_line = 0
                pad_scroll = 0
                out_pad.refresh(0, 0, 0, 0, OUTPUT_HEIGHT - 1, max_w - 1)
                continue

            # Route the message
            eval1 = router.eval_user_input(message)

            if eval1 == "Action":
                pad_print("Action detected!", curses.color_pair(3))
            elif eval1 == "Not Action":
                token_gen = send_message.message(message, "qwen2.5:3b")

                # Start on a new line, track position within that line
                current_line = ""
                for token in token_gen:
                    for char in token:
                        if char == "\n":
                            pad_print(current_line)  # flush current line
                            current_line = ""
                        else:
                            current_line += char
                            # Write char directly to pad at current position
                            try:
                                out_pad.addstr(pad_line, len(current_line) - 1, char, curses.color_pair(4))
                            except curses.error:
                                pass
                    # Refresh pad after each token so it appears live
                    out_pad.refresh(pad_scroll, 0, 0, 0, OUTPUT_HEIGHT - 1, max_w - 1)

                if current_line:  # flush any remaining text
                    pad_print(current_line)
            else:
                pad_print(f"Unknown message type: {eval1}", curses.color_pair(3))

            pad_print("")

        # Backspace
        elif code in (8, 127, curses.KEY_BACKSPACE):
            if input_buf:
                input_buf.pop()

        # Scroll output up
        elif code == curses.KEY_UP:
            if pad_scroll > 0:
                pad_scroll -= 1
                out_pad.refresh(pad_scroll, 0, 0, 0, OUTPUT_HEIGHT - 1, max_w - 1)

        # Scroll output down
        elif code == curses.KEY_DOWN:
            visible_lines = OUTPUT_HEIGHT - 1
            if pad_scroll < pad_line - visible_lines:
                pad_scroll += 1
                out_pad.refresh(pad_scroll, 0, 0, 0, OUTPUT_HEIGHT - 1, max_w - 1)

        # Printable characters
        elif isinstance(ch, str) and ch.isprintable():
            input_buf.append(ch)

        elif code >= 32:
            input_buf.append(chr(code))


if __name__ == "__main__":
    curses.wrapper(main)