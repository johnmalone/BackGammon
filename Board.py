from copy import deepcopy
from pprint import pprint

import copy
import logging
logging.basicConfig(filename='/tmp/curses.log',level=logging.DEBUG)

class Board () :
    errors = []

    MY_JAIL = 1
    HIS_JAIL = 28

    MY_HOME = 2
    HIS_HOME = 27

    MY_ACE = 3
    HIS_ACE = 26

    def __init__(self):
        self.doubleCube = {'player': False, 'value': 1 }
        self.score = {'1': 0, '2': 0}

    def setDefaultBoardState(self):
        state = []

        state.insert(0, -9999)
        state.insert(1, 0)
        state.insert(2, 0)
        state.insert(3, 2)
        state.insert(4, 0)
        state.insert(5, 0)
        state.insert(6, 0)
        state.insert(7, 0)
        state.insert(8, -5)
        state.insert(9, 0)
        state.insert(10, -3)
        state.insert(11, 0)
        state.insert(12, 0)
        state.insert(13, 0)
        state.insert(14, 5)
        state.insert(15, -5)
        state.insert(16, 0)
        state.insert(17, 0)
        state.insert(18, 0)
        state.insert(19, 3)
        state.insert(20, 0)
        state.insert(21, 5)
        state.insert(22, 0)
        state.insert(23, 0)
        state.insert(24, 0)
        state.insert(25, 0)
        state.insert(26, -2)
        state.insert(27, 0)
        state.insert(28, 0)
        state.insert(29, 9999) # which way is up?

        self.setCustomBoardState(state,  1)

    def setCustomBoardState(self, boardState, turn):
        self.turn = turn
        self.board =  boardState

    def getPipAtIdx(self,idx):
        self.setBoardForPlayer(1)
        return self.board[self.MY_ACE+idx]

    def getJailCountForPlayer(self,player):
        self.setBoardForPlayer(player)
        return abs(self.board[self.MY_JAIL])

    def getHomeCountForPlayer(self,player):
        self.setBoardForPlayer(player)
        return abs(self.board[self.MY_HOME])

    def userError(self, msg):
        logging.debug(msg)
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
        self.turn *= -1

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

    """ Incoming moves from view are:
        1->24: pip
        jail
        home
        convert the incoming position to an index 
        from POV of self.turn"""
    def convertViewPosToIdx(self, viewPos):
        if viewPos == 'jail':
            return self.MY_JAIL
        elif viewPos == 'home':
            return self.MY_HOME
        elif int(viewPos) >= 1 or int(viewPos) <= 24:
            if self.turn > 0:
                return self.MY_ACE+(int(viewPos)-1)
            else:
                return self.MY_ACE+(24 - int(viewPos))
        else:
            return False

    def resetView(self):
        if self.board[0] == 9999:
           list(reversed(self.board))

    def setBoardForPlayer(self, player):
        if player > 0:
            if self.board[0] != 9999:
                self.board = list(reversed(self.board))
        else:
             if self.board[0] != -9999:
                self.board = list(reversed(self.board))
        return

    def playerHasMoveAvailable(self):
        self.setBoardForPlayer(self.turn)
        if self.board[self.MY_JAIL] != 0:
            for i,die in enumerate(self.dice):
                if self.canPieceMoveOutOfJail(die):
                    return True
            return False

        for pos in range(self.MY_ACE, self.MY_ACE+24):
            pip = self.board[pos]
            if (self.turn > 0) != (pip > 0):
                continue
            for i,die in enumerate(self.dice):
                destPip = pos - die
                logging.debug('destPip {0}, pos:{1}'.format(destPip,pos))
                if destPip > self.MY_ACE+23:
                    destPip = self.MY_HOME
                if self.canPieceMoveToPosition(pos, destPip):
                    return True
        return False

    def getPipCount(self) :
        pipCount = {'1': 0, '-1': 0}
        for player in [-1, 1]:
            self.setBoardForPlayer(player)
            for pos,count in enumerate(self.board):
                if (count > 0) != (player > 0):
                    continue
                if pos == 0:
                    continue
                elif pos == self.MY_JAIL:
                    pipCount[str(player)] += abs(count*25)
                elif pos < self.MY_ACE+24:
                    pipCount[str(player)] += abs(count*(pos-(self.MY_ACE-1)))

        return pipCount

    def canPieceMoveOutOfJail(self, dice):
        self.setBoardForPlayer(self.turn)

        movingPlayer = self.turn
        if self.board[self.MY_JAIL]:
            if dice > 6:
                self.userError('Piece in Jail not moved correctly')
                return False

        if self.doesPositionHave2OrMoreOppostionPieces(dice, movingPlayer) :
            self.userError('2 or more opposing pieces at new position')
            return False

        return True

    """ positions should be 0 indexed.
        1 == jail
        2 == home
        opp Ace point = 23"""
    def canPieceMoveToPosition(self, oldPosIdx, newPosIdx) :
        if not oldPosIdx or not newPosIdx:
            self.userError('Illegal pip error')
            return False

        self.setBoardForPlayer(self.turn)
        if not self.board[oldPosIdx] :
            self.userError('No pieces at old position')
            return False
        if (self.board[oldPosIdx] > 0) != (self.turn > 0):
            self.userError('You cant move the opposition pieces')
            return False

        if self.board[self.MY_JAIL] and oldPosIdx != self.MY_JAIL:
            self.userError('you must move out of jail first')
            return False

        if newPosIdx == self.MY_HOME :
            if self.turn == -1:
                start = 0
                end = 18
            else :
                start = 6
                end = 24

            for i in range(start,end) :
                if self.doesPositionHaveSameTypeOfPiece(i, self.turn) :
                    self.userError('Pieces cant be moved off until all pieces \
                            are in the last 6 places for that player.')
                    return False
            return True # needs testing

        if self.doesPositionHave2OrMoreOppostionPieces(newPosIdx, self.turn) :
            self.userError('2 or more opposing pieces at new position')
            return False

        # internally we might move things to jail
        if newPosIdx == self.MY_JAIL:
            return True

        if oldPosIdx < newPosIdx :
            self.userError('Pieces can only move forward')
            return False

        if oldPosIdx == self.MY_HOME:
            self.userError('Piece cant move out of home')
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
        if int(pip) < 23:
            return True

        self.userError('Illegal pip')
        return False

    """ Accepts view pov positions and returns true if the piece was moved
        successfully, false otherwise"""
    def movePiece (self, player, oldPosition, newPosition) :
        oldPosIdx = self.convertViewPosToIdx(oldPosition)
        newPosIdx = self.convertViewPosToIdx(newPosition)
        if not oldPosIdx or not newPosIdx:
            self.userError('Illegal pip error')
            return False

        self.setBoardForPlayer(self.turn)

        if not self.canPieceMoveToPosition(oldPosIdx, newPosIdx) :
            self.userError('Cant move to that position')
            return False

        if oldPosIdx != self.MY_JAIL and newPosIdx != self.MY_HOME:
            if not self.doesPositionHaveSameTypeOfPiece(oldPosIdx, player):
                self.userError('Its not your turn!!')
                return False

            posDiff = abs(oldPosIdx - newPosIdx)
            if not self.areDiceLegit(posDiff) :
                self.userError('Dice are not legit')
                return False
            self.dice.remove(posDiff)

            if self.board[newPosIdx] == 1 or self.board[newPosIdx] == -1:
                self.board[self.HIS_JAIL] -= player
                self.board[newPosIdx] += player
            self.board[oldPosIdx] -= player
            self.board[newPosIdx] += player

        elif newPosIdx == self.MY_HOME:
            #changed from previous version. logic different...
            for i,diceInList in enumerate(self.dice):
                logging.debug(diceInList)
                logging.debug(oldPosIdx)
                if diceInList >= (oldPosIdx - (self.MY_ACE-1)):
                    self.dice.remove(diceInList)
                    self.board[int(oldPosIdx)] -= player
                    self.board[self.MY_HOME] += player
                    return True
            return False

        else:
            for i,diceInList in enumerate(self.dice):
                if not self.canPieceMoveOutOfJail(diceInList) :
                    return False

            if not self.areDiceLegit(oldPosition) :
                return False

            self.board[self.MY_JAIL] -= player
            if self.board[newPosIdx] > 1 or self.board[newPosIdx] < -1:
                self.board[self.HIS_JAIL] -= player
            self.board[newPosIdx] += player

            self.dice.remove(posDiff)

        return True

    def getActiveDice(self):
        return self.dice

    def gameIsOver(self):
        pipCount = self.getPipCount()
        if not pipCount['1']:
            self.userError('Player 1 is the winner!')
            return True
        elif not pipCount['-1'] :
            self.userError('Player 2 is the winner!')
            return True
        return False

    def setDiceRoll(self, dice):
        self.dice = dice

    """0 indexed"""
    def doesPositionHaveSameTypeOfPiece(self, posIdx, player) :
        if not self.board[posIdx]:
            return False
        if (self.board[posIdx] < 0) != (player < 0):
            return False
        return True

    """Accepts view positions (1->24)"""
    def doesPositionHave2OrMoreOppostionPieces(self, posIdx, player):
        if self.board[posIdx] > -2 and self.board[posIdx] < 2:
            return False

        return self.doesPositionHaveSameTypeOfPiece(posIdx, player*-1)

