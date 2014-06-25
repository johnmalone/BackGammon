from Board import Board
from CursesBoardView import CursesBoard, bgBoard
from pprint import pprint
from time import sleep
import curses, curses.panel
from GameController import GameController

state = []

state.insert(0, ['2'])
state.insert(1, [])
state.insert(2, [])
state.insert(3, [])
state.insert(4, [])
state.insert(5, [])
state.insert(6, [])
state.insert(7, [])
state.insert(8, [])
state.insert(9, [])
state.insert(10, [])
state.insert(11, [])
state.insert(12, [])
state.insert(13, [])
state.insert(14, [])
state.insert(15, [])
state.insert(16, [])
state.insert(17, [])
state.insert(18, [])
state.insert(19, [])
state.insert(20, [])
state.insert(21, [])
state.insert(22, [])
state.insert(23, ['1'])

jail = {1: ['1', '1', '1','1'], 2: ['2','2','2','2','2']}

gc = GameController()
#gc.setCustomBoardState(state, jail, 1)
gc.gameLoop()


