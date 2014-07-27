import copy
import logging
import random
logging.basicConfig(filename='/tmp/curses.log',level=logging.DEBUG)

class BGEngine():

    def __init__(self,board):
        self.board = copy.deepcopy(board)
        self.bestMove = False
        self.bestScore = 100000

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
        analyseBoard = AnalyseBoard(board, move)
        boardScore = analyseBoard.getBoardScoreForPlayer(player)
        if boardScore < self.bestScore:
            self.bestMove = move

    def addMove(self, move, board,player):
        self.analyseMove(move, board,player)

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
        homeCheck = board.canPlayerMoveOff(player)
        jail = board.isPlayerInJail(player)
        board.setBoardForPlayer(player)
        state = board.board
        for die in dice:

            if jail:
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

            if homeCheck:
                if player == 1:
                    lastFewPips = list(range(6,0,-1))
                else:
                    lastFewPips = list(range(19,25))

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

            for pip in pipList:
                pipIdx = board.convertViewPosToIdx(pip)
                if board.doesPositionHaveSameTypeOfPiece(pipIdx,player):
                    diceToPassOn = copy.deepcopy(dice)
                    cloneBoard = copy.deepcopy(board)
                    if player == 1:
                        newPip = pip - die
                    else :
                        newPip = pip + die
                    if newPip <= 0:
                        continue
                    if newPip >= 25:
                        continue
                    if cloneBoard.movePiece(player, pip, newPip):
                        cloneMove = copy.deepcopy(move)
                        cloneMove.append((pip, newPip))
                        diceToPassOn.remove(die)
                        self.genMoves(cloneBoard, player, diceToPassOn, cloneMove,doubles,pip)
                        moveTried = True

        # if we end up using less than our dice pass up a move with less than
        # the full amount
        if not moveTried and move:
                self.addMove(move, board,player)


class AnalyseBoard():
    def __init__(self, board, move):
        self.board = board
        self.move = move

    def getBoardScoreForPlayer(self, player):
        pipDiff = self.getPipCountDiff(player)
        blotScore = self.getBlotDanger(player)
        runOfDoubles, doubleCount = self.getBlockersAndDoubles(player)
        moveOffScore = self.prioritizeMovingOff(player)
        return pipDiff + blotScore + runOfDoubles + doubleCount + moveOffScore

    def prioritizeMovingOff(self,player):
        moveOffScore = 0
        if self.board.canPlayerMoveOff(player):
            if [oneMove for oneMove in self.move if oneMove[1] == 'home']:
                moveOffScore -= 1000
        return moveOffScore

    def getBlockersAndDoubles(self, player):
        doubleCount = 0
        runOfDoubles = 0
        maxDoubleCount = doubleCount
        runOfDoubles = False
        for idx in self.board.getOutFieldRange():
            if self.board.doesPositionHaveSameTypeOfPiece(idx,player):
                if abs(self.board.board[idx]) >= 2:
                    runOfDoubles = True
                else:
                    runOfDoubles = False
            else:
                    runOfDoubles = False

            if runOfDoubles:
                doubleCount += 1
                runOfDoubles += 1
                if runOfDoubles > maxDoubleCount:
                    maxDoubleCount = runOfDoubles
            else:
                runOfDoubles = 0
        return -1 * 4 * maxDoubleCount, -1 * 8 * doubleCount


    def getPipCountDiff(self,player):
        pipCount = self.board.getPipCount()
        if player == 1:
            pipDiff = pipCount[str(player)] - pipCount['-1']
        else :
            pipDiff = pipCount[str(player)] - pipCount['1']
        return pipDiff

    def getBlotDanger(self, player):
        idxForBlots = []
        for idx in self.board.getOutFieldRange():
            if self.board.doesPositionHaveBlotForPlayer(idx, player):
                if self.isBlotInDanger(idx, player):
                    idxForBlots.append(idx)
        return 4 * len(idxForBlots)

    def isBlotInDanger(self,blotIdx, player):
        myList = list(self.board.getOutFieldRange())
        for idx in myList[::-1]:
            if idx < blotIdx:
                if not self.board.doesPositionHaveSameTypeOfPiece(idx,player):
                    if abs(self.board.board[idx]) == 1:
                        blotDiff = blotIdx - idx
                        if blotDiff < 12 or blotDiff in [15, 20, 24]:
                            return True
        return False
