from Board import Board
from CursesBoardView import CursesBoard, bgBoard
from pprint import pprint
from time import sleep
import curses, curses.panel
from GameController import GameController

state = []

state.insert(0, -9999)
state.insert(1, -0) #  -1 jail
state.insert(2, -0) #  -1 home
state.insert(3, 0)
state.insert(4, 0)
state.insert(5, 0)
state.insert(6, 0)
state.insert(7, 0)
state.insert(8, 0)
state.insert(9, 0)
state.insert(10, 0)
state.insert(11, 2)
state.insert(12, 1)
state.insert(13, 2)
state.insert(14, 2)
state.insert(15, 0)
state.insert(16, 0)
state.insert(17, 0)
state.insert(18, -2)
state.insert(19, -1)
state.insert(20, -2)
state.insert(21, -2)
state.insert(22, 0)
state.insert(23, 0)
state.insert(24, 0)
state.insert(25, 0)
state.insert(26, 0)
state.insert(27, 0) # 1 home
state.insert(28, 0) # 1 jail
state.insert(29, 9999)

gc = GameController()
#gc.setCustomBoardState(state, 1)
gc.gameLoop()


