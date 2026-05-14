import curses


class ChatUI:
    INPUT_BOX_HEIGHT = 3
    PAD_HEIGHT = 1000

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.max_h, self.max_w = stdscr.getmaxyx()
        self.output_height = self.max_h - self.INPUT_BOX_HEIGHT
        self.pad_scroll = 0
        self.pad_line = 0

        self._setup_colors()
        self._setup_windows()

    def _setup_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)    # borders
        curses.init_pair(2, curses.COLOR_GREEN, -1)   # prompt
        curses.init_pair(3, curses.COLOR_YELLOW, -1)  # system messages
        curses.init_pair(4, curses.COLOR_WHITE, -1)   # normal output

    def _setup_windows(self):
        self.out_pad = curses.newpad(self.PAD_HEIGHT, self.max_w)
        self.out_pad.scrollok(True)
        self.in_win = curses.newwin(self.INPUT_BOX_HEIGHT, self.max_w, self.output_height, 0)

    def print(self, text, attr=curses.A_NORMAL):
        """Print a line to the output pad, auto-scrolling to bottom."""
        chunks = [text[i:i + self.max_w - 1] for i in range(0, max(len(text), 1), self.max_w - 1)]
        for chunk in chunks:
            try:
                self.out_pad.addstr(self.pad_line, 0, chunk, attr)
            except curses.error:
                pass
            self.pad_line += 1

        visible_lines = self.output_height - 1
        if self.pad_line > visible_lines:
            self.pad_scroll = self.pad_line - visible_lines
        self._refresh_pad()

    def print_token(self, char, col):
        """Write a single character in-place on the current output line."""
        try:
            self.out_pad.addstr(self.pad_line, col, char, curses.color_pair(4))
        except curses.error:
            pass
        self._refresh_pad()

    def flush_line(self, line):
        """Commit a completed streamed line to the pad."""
        self.print(line)

    def clear_output(self):
        self.out_pad.clear()
        self.pad_line = 0
        self.pad_scroll = 0
        self._refresh_pad()

    def scroll_up(self):
        if self.pad_scroll > 0:
            self.pad_scroll -= 1
            self._refresh_pad()

    def scroll_down(self):
        visible_lines = self.output_height - 1
        if self.pad_scroll < self.pad_line - visible_lines:
            self.pad_scroll += 1
            self._refresh_pad()

    def _refresh_pad(self):
        self.out_pad.refresh(self.pad_scroll, 0, 0, 0, self.output_height - 1, self.max_w - 1)

    def refresh_input(self, current_text=""):
        self.in_win.clear()
        _, w = self.in_win.getmaxyx()
        border = "=" * w
        try:
            self.in_win.addstr(0, 0, border, curses.color_pair(1))
            self.in_win.addstr(2, 0, border[: w - 1], curses.color_pair(1))
        except curses.error:
            pass
        prompt = "> "
        self.in_win.addstr(1, 0, prompt, curses.color_pair(2) | curses.A_BOLD)
        self.in_win.addstr(1, len(prompt), current_text, curses.color_pair(4))
        self.in_win.move(1, len(prompt) + len(current_text))
        self.in_win.refresh()

    def get_char(self):
        return self.in_win.get_wch()

    def colour(self, pair):
        return curses.color_pair(pair)

    @property
    def BOLD(self):
        return curses.A_BOLD