from Board import Board
from CursesBoardView import CursesBoard, bgBoard
from pprint import pprint
from time import sleep
import curses, curses.panel

board = Board()
board.setDefaultBoardState()
board.setTurn(1)

#board.movePiece(0,1)
#board.movePiece(5,1)
#if not board.movePiece(11,10):
 #   print ("Failed to move piece!")
  #  print ("\n".join(board.getErrorsList()))
#board.movePiece(11,9)
#board.movePiece(11,8)

#board.movePiece(7,10)
#board.movePiece(7,9)
#board.movePiece(7,8)
#board.movePiece(0,8)
board.getPipCount()
state = board.getBoardState()
jail = board.getJail()
home = board.getHome()

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

boardView = CursesBoard(stdscr)
boardView.addState(state)
boardView.addJail(jail)
boardView.addHome(home)
boardView.addDice(2,4)
boardView.createBoard()

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

