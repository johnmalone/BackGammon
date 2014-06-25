import curses, curses.panel
import logging

logging.basicConfig(filename='/tmp/curses.log',level=logging.DEBUG)


class CursesBoard () :
    def make_panel(self, h,l, y,x, str):
        win = curses.newwin(h,l, y,x)
        win.erase()
        win.box()
        win.addstr(2, 2, str)

        panel = curses.panel.new_panel(win)
        return win, panel

    def draw_pips_on_line(self, win, y, x, boxWidth, boxHeight) :
        pipWidth = boxWidth / 6
        firstPipCoord = x + (pipWidth/2)
    
        for xPoint in range(int(firstPipCoord), boxWidth, int(pipWidth)) :
            logging.debug(xPoint)
            logging.debug(boxWidth)
            logging.debug(pipWidth)

            win.addch(y, xPoint, curses.ACS_VLINE)

    def draw_checker_at_pip(self, win, pip, player) :
        pass


    def createBoard(self, stdscr):
        try:
            curses.curs_set(0)
        except:
            pass
        win1, panel1 = self.make_panel(40, 150, 0, 0, "Main Board")
        win2, panel2 = self.make_panel(30, 60, 5, 10, "")
        win3, panel3 = self.make_panel(30, 60, 5, 75, "")
        win4, panel4 = self.make_panel(15, 10, 5, 135, "Panel 4")
        win5, panel5 = self.make_panel(15, 10, 20,135, "Panel 5")
        self.draw_pips_on_line(win2, 0, 0, 60, 10)
        self.draw_pips_on_line(win2, 29, 0, 60, 10)
        self.draw_pips_on_line(win3, 0, 0, 60, 10)
        self.draw_pips_on_line(win3, 29, 0, 60, 10)
        curses.panel.update_panels(); stdscr.refresh()
        stdscr.getkey()


def main(stdscr) :
    screen

if __name__ == '__main__':
    curses.wrapper(main)

