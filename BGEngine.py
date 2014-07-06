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
        return True # dumb things down for a while...
        if not self.bestMove:
            return True
        else :
            pipCount = board.getPipCount()
            if player == 1:
                pipDiff = pipCount[str(player)] - pipCount['-1']
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

        if doubles and lastPipIdx:
            if player == 1:
                pipList = list(range(1,lastPipIdx))
            else:
                pipList = list(range(lastPipIdx,1, -1))
        else:
            if player == 1:
                pipList = list(range(1,25))
            else:
                pipList = list(range(24,0,-1))
        homeCheck = True
        jail = board.isPlayerInJail(player)
        board.setBoardForPlayer(player)
        state = board.board
        for die in dice:

            if jail:
                homeCheck = False
                cloneBoard = copy.deepcopy(board)
                diceToPassOn = copy.deepcopy(dice)
                if player == 1:
                    newPip = 25 - die
                else:
                    newPip = die

                if cloneBoard.movePiece(player, 'jail', newPip):
                    cloneMove = copy.deepcopy(move)
                    cloneMove.append(('jail', newPip))
                    diceToPassOn.remove(die)
                    self.genMoves(cloneBoard, player, diceToPassOn,cloneMove,doubles)
                    moveTried = True
                    # continue here??
                    # we started in jail so no point in doing the stuff below

            for pip in pipList:
                pipIdx = board.convertViewPosToIdx(pip)
                if board.doesPositionHaveSameTypeOfPiece(pipIdx,player):
                    if player == 1 and pip > 6:
                        homeCheck = False
                    elif player == -1 and pip < 17:
                        homeCheck = False
                    diceToPassOn = copy.deepcopy(dice)
                    cloneBoard = copy.deepcopy(board)
                    if player == 1:
                        newPip = pip - die
                    else :
                        newPip = pip + die
                    if cloneBoard.movePiece(player, pip, newPip):
                        cloneMove = copy.deepcopy(move)
                        cloneMove.append((pip, newPip))
                        diceToPassOn.remove(die)
                        self.genMoves(cloneBoard, player, diceToPassOn, cloneMove,doubles,pip)
                        moveTried = True

            if homeCheck:
                if player == 1:
                    lastFewPips = list(range(19,24))
                else:
                    lastFewPips = list(range(5,-1,-1))

                for pip in lastFewPips:
                    pipIdx = board.convertViewPosToIdx(pip)
                    if board.doesPositionHaveSameTypeOfPiece(pipIdx,player):
                        diceToPassOn = copy.deepcopy(dice)
                        cloneBoard = copy.deepcopy(board)
                        if cloneBoard.movePiece(player, pip, 'home'):
                            cloneMove = copy.deepcopy(move)
                            cloneMove.append((pip, 'home'))
                            diceToPassOn.remove(die)
                            self.genMoves(cloneBoard, player, diceToPassOn, cloneMove,doubles,pip)
                            moveTried = True
        # if we end up using less than our dice pass up a move with less than
        # the full amount
        if not moveTried and move:
                self.addMove(move, board,player)
