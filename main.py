import router
import curses

from utils import send_message

def get_input(stdscr):
    border = "=" * 20
    stdscr.addstr(0, 0, border)
    stdscr.addstr(1, 0, "> ")
    stdscr.addstr(2, 0, border)
    stdscr.move(1, 2)  

    curses.echo()
    user_input = stdscr.getstr(1, 2).decode("utf-8")
    return user_input

def main():
    while True:
        message = curses.wrapper(get_input)

        if message == "/exit":
            print("Bai")
            break
        
        if message == "":
            continue

        if message == "/clear":
            print("\033c", end="")
            continue

        eval1 = router.eval_user_input(message)

        if eval1 == "Action":
            print("Action detected!")
        elif eval1 == "Not Action":
            print("Normal message detected!")
        else:
            print("Unknown message type detected!", eval1)

if __name__ == "__main__":
    main()