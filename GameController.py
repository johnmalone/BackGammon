from Board import Board
from CursesBoardView import CursesBoard, bgBoard
from pprint import pprint
from time import sleep
from BGEngine import BGEngine

import curses, curses.panel
import logging
import re
import random
import copy

logging.basicConfig(filename='/tmp/curses.log',level=logging.DEBUG)

class GameController():
    def __init__(self):
        self.board = Board()
        self.board.setDefaultBoardState()
        self.initCurses()
        self.boardView = CursesBoard(self.stdscr)

    def setCustomBoardState(self, state, jail, turn):
        self.board.setCustomBoardState(state, jail, turn)

    def initCurses(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def cleanUpCurses(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def setupBoardView(self, dice = False):
        activeDice = self.board.getActiveDice()
        self.boardView.setActiveDice(copy.deepcopy(activeDice))
        self.boardView.addBoardObj(self.board)
        if not dice:
            self.boardView.addDice(copy.deepcopy(activeDice))
        else :
            self.boardView.addDice(copy.deepcopy(dice))
        self.boardView.createBoard(self.board.getTurn())

    def doDiceRoll(self):
        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        if d1 == d2:
            return [d1, d2, d1, d2]
        else :
            return [d1, d2]

    def doMove(self, player, sourceDest) :
        source, dest = re.split('\s', sourceDest)
        r = self.board.movePiece(player, source, dest)
        if not r :
            errors = self.board.getErrorsList()
            return False
        else :
            return True
        return True

    def doHumanMove(self):
        inputStr = self.boardView.getUserInput().decode('ascii').strip()
        error = False
        self.boardView.addErrorMessage('')
        if inputStr == 'q' :
            self.cleanUpCurses()
            quit()
        if re.search('^(jail|\d{1,2})\s(\d{1,2}|home)$',inputStr) :
            if not self.doMove(self.board.getTurn(), inputStr):
                self.boardView.addErrorMessage(self.board.getRecentError())
                error = True
        else:
            self.boardView.addErrorMessage('Bad command. <start pip> <end pip>. Enter move> ')
            error = True
        return error

    def doComputerMove(self, move, dice, testing = False):
        error = False
        for oneMove in move:
            moveStr = " ".join(str(i) for i in oneMove)
            if not self.doMove(self.board.getTurn(), moveStr):
                error = True
                return error
            self.boardView.addPromptText('Computer move> {0}'.format(moveStr))
            self.setupBoardView(dice)
            if not testing:
                sleep(2.5)
        self.boardView.addPromptText(False)
        return error

    def gameLoop(self):
        random.seed();
        dice = self.doDiceRoll()
        self.board.setDiceRoll(copy.deepcopy(dice))
        self.setupBoardView()
        self.boardView.addPromptText('(h)uman; (c)omputer; (t)est; (q)uit?> ')
        testing = False
        computer = False
        human = False

        while True:
            self.setupBoardView()
            inputStr = self.boardView.getUserInput().decode('ascii').strip()
            if inputStr in ['c', 'C']:
                computer = True
                break
            elif inputStr in ['h', 'H']:
                human = True
                break
            elif inputStr in ['t', 'T']:
                testing = True
                break
            elif inputStr in ['q', 'Q']:
                self.cleanUpCurses()
                return True
            else:
                self.boardView.addPromptText('(h)uman; (c)omputer; (t)est; (q)uit?> ')

        self.boardView.addPromptText(False)
        self.setupBoardView()

        while True:
            if not self.board.playerHasMoveAvailable():
                self.boardView.addErrorMessage('Player {0} has no moves available with dice {1},{2}!'\
                                                .format(self.board.getTurn(), dice[0], dice[1] ))
                self.board.toggleTurn()
                dice = self.doDiceRoll()
                self.board.setDiceRoll(copy.deepcopy(dice))
                self.board.clearErrors()
                self.setupBoardView()
                sleep (1)
                continue
            if self.board.getTurn() == 1:
                if testing:
                    bgEngine = BGEngine(copy.deepcopy(self.board))
                    bgEngine.addDice(copy.deepcopy(self.board.getActiveDice()))
                    move = bgEngine.getMoveForPlayer(self.board.getTurn())
                    error = self.doComputerMove(move, dice, testing)
                else:
                    error = self.doHumanMove()
            else:
                if human :
                    error = self.doHumanMove()
                elif computer or testing:
                    if not testing:
                        sleep(1)
                    bgEngine = BGEngine(copy.deepcopy(self.board))
                    bgEngine.addDice(copy.deepcopy(self.board.getActiveDice()))
                    move = bgEngine.getMoveForPlayer(self.board.getTurn())
                    error = self.doComputerMove(move, dice,testing)

            if not error and self.board.gameIsOver():
                self.boardView.addErrorMessage(self.board.getRecentError())
                self.board.clearErrors()
                self.boardView.addState(self.board.getBoardState())
                self.boardView.createBoard(self.board.getTurn())
                return True

            if not error and self.board.turnIsOver():
                self.board.toggleTurn()
                dice = self.doDiceRoll()
                self.board.setDiceRoll(copy.deepcopy(dice))
                self.boardView.addDice(copy.deepcopy(dice))

            self.board.clearErrors()
            self.setupBoardView(dice)


