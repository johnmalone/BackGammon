from Piece import Piece
from Pip import Pip
from copy import deepcopy
from pprint import pprint

import copy
import logging
logging.basicConfig(filename='/tmp/curses.log',level=logging.DEBUG)


class Board () :
    errors = []
    def __init__(self):
        self.doubleCube = {'player': False, 'value': 1 }
        self.score = {'1': 0, '2': 0}

    def setDefaultBoardState(self):
        state = []

        state.insert(0, ['1','1'])
        state.insert(1, [])
        state.insert(2, [])
        state.insert(3, [])
        state.insert(4, [])
        state.insert(5, ['2','2','2','2','2'])
        state.insert(6, [])
        state.insert(7, ['2','2','2'])
        state.insert(8, [])
        state.insert(9, [])
        state.insert(10, [])
        state.insert(11, ['1','1','1','1','1'])
        state.insert(12, ['2','2','2','2','2'])
        state.insert(13, [])
        state.insert(14, [])
        state.insert(15, [])
        state.insert(16, ['1','1','1'])
        state.insert(17, [])
        state.insert(18, ['1','1','1','1','1'])
        state.insert(19, [])
        state.insert(20, [])
        state.insert(21, [])
        state.insert(22, [])
        state.insert(23, ['2','2'])

        jail = {1: [], 2: []}

        self.setCustomBoardState(state, jail, 1)

    def setCustomBoardState(self, boardState, jail, turn):
        self.jail = {1: [], 2: []}
        self.home = {1: [], 2: []}
        self.turn = turn

        for player in jail:
            for pips in enumerate(jail[player]):
                piece = Piece()
                if player == 1:
                    piece.setPlayer1()
                else:
                    piece.setPlayer2()
                self.jail[player].append(piece)

        self.board = []
        for pos,pips in enumerate(boardState):
            pip = Pip()
            if not pips:
                self.board.insert(pos,pip)
                continue

            player = pips[0]
            count = len(pips)
            for i in range(count):
                piece = Piece()
                if player == '1':
                    piece.setPlayer1()
                else:
                    piece.setPlayer2()
                pip.addPieceToPip(piece)

            self.board.insert(pos,pip)

    def userError(self, msg):
        self.errors.insert(0,msg)

    def clearErrors(self):
        self.errors = []

    def getErrorsList(self):
        return self.errors

    def getRecentError(self):
        if self.errors:
            return self.errors[0]

    def getBoardState(self) :
        return self.board

    def setTurn(self, player=1) :
        self.turn = player

    def toggleTurn(self) :
        self.turnOver = False
        if self.turn == 1 : 
            self.turn = 2
        elif self.turn == 2 :
            self.turn = 1

    def getTurn(self):
        return self.turn

    def doubleCube(self, acceptingPlayer):
        if self.doubleCube[acceptingPlayer] == accpetingPlayer:
            self.userError('Player already has double cube. Other player must double')
            return False
        self.doubleCube[acceptingPlayer] = acceptingPlayer
        self.doubleCube['value'] *= 2
        return True

    def getDoubleCube(self) :
        return self.doubleCube

    def getJail(self):
        return self.jail

    def getHome(self):
        return self.home

    def playerHasMoveAvailable(self):
        if self.jail[self.turn]:
            for i,die in enumerate(self.dice):
                if self.turn == 1:
                    destPip = die - 1
                if self.turn  == 2:
                    destPip = 24 - die
                if self.canPieceMoveOutOfJail('jail', destPip):
                    return True
            return False

        for pos,pip in enumerate(self.board):
            if self.turn != pip.getPlayerOnPip():
                continue
            for i,die in enumerate(self.dice):
                if self.turn == 1:
                    destPip = pos + die
                elif self.turn == 2:
                    destPip = pos - die

                if destPip < 0 or destPip > 23:
                    destPip = 'home'
                if self.canPieceMoveToPosition(pos, destPip):
                    return True

        self.userError('Player %s has no valid moves. Turn Over.' % self.turn)
        return False

    def getPipCount(self) :
        pipCount1 = 0
        pipCount2 = 0
        pipCount1 += len(self.jail[1]) * 25
        pipCount2 += len(self.jail[2]) * 25

        for pos, pip in enumerate(self.board) :
            if pip.getPipCount() :
                if pip.getPlayerOnPip() == 1:
                    pipCount1 += (24-pos) * pip.getPipCount()
                else:
                    pipCount2 += (1+pos) * pip.getPipCount()

        return {'1' : pipCount1, '2' : pipCount2 }

    def canPieceMoveOutOfJail(self, oldPosition, newPosition):
        jailError = False
        movingPlayer = self.turn
        if self.jail[movingPlayer] :
            if oldPosition != 'jail':
                jailError = True
            if movingPlayer == 1 and newPosition > 5 :
                jailError = True
            if movingPlayer == 2 and newPosition < 19: 
                jailError = True

        if jailError :
            self.userError('Piece in Jail not moved correctly')
            return False

        if self.doesPositionHave2OrMoreOppostionPieces(newPosition, movingPlayer) :
            self.userError('2 or more opposing pieces at new position')
            return False

        return True

    def canPieceMoveToPosition(self, oldPosition, newPosition) :
        if not self.isPipLegal(oldPosition) or not self.isPipLegal(newPosition):
            self.userError('Illegal pip error')
            return False

        if not self.board[oldPosition].getPipCount() :
            self.userError('No pieces at old position')
            return False

        if oldPosition < 0 or oldPosition > 23 :
            self.userError('Invalid old position given.')
            return False

        movingPlayer = self.board[oldPosition].getPlayerOnPip()
        if movingPlayer != self.turn:
            self.userError('you cant move the other players piece')
            return False

        if self.jail[movingPlayer] and oldPosition != 'jail':
            self.userError('you must move out of jail first')
            return False

        if newPosition == 'home' :
            if movingPlayer == 1:
                start = 0
                end = 18
            else :
                start = 6
                end = 24

            for i in range(start, end) :
                if self.doesPositionHaveSameTypeOfPiece(i, movingPlayer) :
                    self.userError('Pieces cant be moved off until all pieces \
                            are in the last 6 places for that player.')
                    return False
            return True # needs testing

        if movingPlayer == 1 and oldPosition > newPosition or \
            movingPlayer == 2 and oldPosition < newPosition :
            self.userError('Pieces can only move forward')
            return False

        if newPosition == 'jail':
            return True

        if oldPosition == 'home':
            self.userError('Piece cant move out of home')
            return False

        if self.doesPositionHave2OrMoreOppostionPieces(newPosition, movingPlayer) :
            self.userError('2 or more opposing pieces at new position')
            return False

        return True

    def turnIsOver(self):
        if self.dice:
            return False

        return True

    def areDiceLegit(self, posDiff):

        if not posDiff in self.dice:
            self.userError('Dont have dice for that move')
            return False

        return True

    def isPipLegal(self, pip):
        if pip == 'jail' or pip == 'home':
            return True

        if int(pip) < len(self.board) and int(pip) >= 0:
            return True

        self.userError('Illegal pip')
        return False

    def movePiece (self, player, oldPipNum, newPipNum) :

        if oldPipNum != 'jail' and newPipNum != 'home':
            oldPosition = int(oldPipNum) - 1
            newPosition = int(newPipNum) - 1
            if not self.isPipLegal(oldPosition) or not self.isPipLegal(newPosition):
                return False

            if not self.doesPositionHaveSameTypeOfPiece(oldPosition, player):
                self.userError('Its not your turn!!')
                return False

            if not self.canPieceMoveToPosition(oldPosition, newPosition) :
                return False

            posDiff = abs(oldPosition - newPosition)
            if not self.areDiceLegit(posDiff) :
                return False

            piece = self.board[oldPosition].popPiece()
            possiblyAPiece = self.board[newPosition].addPieceToPip(piece)
            if isinstance(possiblyAPiece,Piece) :
                self.putPieceInJail(possiblyAPiece)

            self.dice.remove(posDiff)

        elif newPipNum == 'home':
            oldPosition = int(oldPipNum) - 1
            newPosition = newPipNum
            if not self.isPipLegal(oldPosition) or not self.isPipLegal(newPosition):
                return False

            if not self.canPieceMoveToPosition(oldPosition, newPosition) :
                return False

            if player == 1:
                posDiff = 25 - int(oldPipNum)
            else:
                posDiff = int(oldPipNum)
            moveOff = False
            for die in reversed(range(posDiff+1)):
                for i,diceInList in enumerate(self.dice):
                    if diceInList == posDiff:
                        self.dice.remove(diceInList)
                        moveOff = True
                        break
                    elif diceInList > posDiff:
                        self.dice.remove(diceInList)
                        moveOff = True
                        break
                if moveOff :
                    break
            if moveOff :
                piece = self.board[oldPosition].popPiece()
                self.home[player].append(piece)
                return True
            else :
                return False


        else:
            oldPosition = oldPipNum
            newPosition = int(newPipNum) - 1
            if not self.isPipLegal(oldPosition) or not self.isPipLegal(newPosition):
                return False

            if not self.canPieceMoveOutOfJail(oldPosition, newPosition) :
                return False

            if player == 1:
                posDiff = int(newPipNum)
            else:
                posDiff = 25 - int(newPipNum)

            if not self.areDiceLegit(posDiff) :
                return False

            piece = self.jail[self.turn].pop()
            possiblyAPiece = self.board[newPosition].addPieceToPip(piece)
            if isinstance(possiblyAPiece,Piece) :
                self.putPieceInJail(possiblyAPiece)

            self.dice.remove(posDiff)

        return True

    def getActiveDice(self):
        return self.dice

    def gameIsOver(self):
        pipCount = self.getPipCount()
        if not pipCount['1']:
            self.userError('Player 1 is the winner!')
            return True
        elif not pipCount['2'] :
            self.userError('Player 2 is the winner!')
            return True
        return False

    def setDiceRoll(self, dice):
        self.dice = dice

    def putPieceInJail(self, piece) :
        self.jail[piece.getPlayer()].append(piece)

    def doesPositionHaveSameTypeOfPiece(self, position, player) :
        if not self.board[position]:
            return False
        if self.board[position].getPlayerOnPip() != player :
            return False
        return True

    def doesPositionHave2OrMoreOppostionPieces(self, position, player):
        if self.board[position].getPipCount() > 1 and self.board[position].getPlayerOnPip() != player :
            return True
        else :
            return False

