import copy
import logging
import random
logging.basicConfig(filename='/tmp/curses.log',level=logging.DEBUG)

class BGEngine():

    def __init__(self,board):
        self.board = copy.deepcopy(board)
        self.bestMove = False
        self.bestPipDiff = -100000

    def addDice(self, dice):
        self.dice = copy.deepcopy(dice)

    def getMoveForPlayer(self, player):
        move = []
        state = copy.deepcopy(self.board)
        if len(self.dice) == 2:
            self.genMoves(copy.deepcopy(state),player,copy.deepcopy(self.dice),move)
            reversedDice = list(reversed(copy.deepcopy(self.dice)))
            self.genMoves( copy.deepcopy(state), player, reversedDice, move)
        else:
            self.genMoves(copy.deepcopy(state),player,copy.deepcopy(self.dice),move,True)
        return self.bestMove

    def analyseMove(self,move,board, player):
        if not self.bestMove:
            return True
        else :
            pipCount = board.getPipCount()
            if player == 1:
                pipDiff = pipCount[str(player)] - pipCount['2']
            else :
                pipDiff = pipCount[str(player)] - pipCount['1']
            if pipDiff > self.bestPipDiff:
                self.bestPipDiff = pipDiff
                return True
            else:
                return False

            if random.randint(1, 100) % 10 == 0 :
                return True
            else:
                return False

    def addMove(self, move, board,player):
        if self.analyseMove(move, board,player):
            self.bestMove = move

    def genMoves(self, board, player, dice, move, doubles = False, lastPipIdx=False):
        moveTried = False
        if not dice:
            self.addMove(move, board, player)
            return

        state = board.getBoardState()
        if doubles and lastPipIdx:
            if player == 1:
                pipList = list(range(0,lastPipIdx))
            else:
                pipList = list(range(lastPipIdx,0, -1))
        else:
            if player == 1:
                pipList = list(range(0,23))
            else:
                pipList = list(range(23,0,-1))
        homeCheck = True
        jail = board.getJail()[player]
        for die in dice:

            if jail:
                homeCheck = False
                cloneBoard = copy.deepcopy(board)
                diceToPassOn = copy.deepcopy(dice)
                if player == 1:
                    newPip = die
                else :
                    newPip = 25 - die

                if cloneBoard.movePiece(player, 'jail', newPip):
                    cloneMove = copy.deepcopy(move)
                    cloneMove.append(('jail', newPip))
                    diceToPassOn.remove(die)
                    self.genMoves(cloneBoard, player, diceToPassOn,cloneMove,doubles,23)
                    moveTried = True

            for pip in pipList:
                if state[pip].getPlayerOnPip() == player:
                    if player == 1 and pip < 17:
                        homeCheck = False
                    elif player == 2 and pip > 6:
                        homeCheck = False
                    diceToPassOn = copy.deepcopy(dice)
                    cloneBoard = copy.deepcopy(board)
                    if player == 1:
                        newPip = pip + die
                    else :
                        newPip = pip - die
                    if cloneBoard.movePiece(player, pip+1, newPip+1):
                        cloneMove = copy.deepcopy(move)
                        cloneMove.append((pip+1, newPip+1))
                        diceToPassOn.remove(die)
                        self.genMoves(cloneBoard, player, diceToPassOn, cloneMove,doubles,pip)
                        moveTried = True

            if homeCheck:
                if player == 1:
                    lastFewPips = list(range(19,24))
                else:
                    lastFewPips = list(range(5,-1,-1))

                for pip in lastFewPips:
                    if state[pip].getPlayerOnPip() == player:
                        diceToPassOn = copy.deepcopy(dice)
                        cloneBoard = copy.deepcopy(board)
                        if cloneBoard.movePiece(player, pip+1, 'home'):
                            cloneMove = copy.deepcopy(move)
                            cloneMove.append((pip+1, 'home'))
                            diceToPassOn.remove(die)
                            self.genMoves(cloneBoard, player, diceToPassOn, cloneMove,doubles,pip)
                            moveTried = True
        # if we end up using less than our dice pass up a move with less than
        # the full amount
        if not moveTried and move:
                self.addMove(move, board,player)
