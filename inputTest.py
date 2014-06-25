if __name__ == "__main__":
    stdscr = curses.initscr()
    stdscr.clear()
    choice = my_raw_input(stdscr, 2, 3, "cool or hot?").lower()
    if choice == "cool":
        stdscr.addstr(5,3,"Super cool!")
    elif choice == "hot":
        stdscr.addstr(5, 3," HOT!") 
    else:
        stdscr.addstr(5, 3," Invalid input") 
    stdscr.refresh()
    stdscr.getch()
    curses.endwin()
