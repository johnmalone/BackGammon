from Board import Board
from BGEngine import BGEngine
import unittest
import copy
import logging
logging.basicConfig(filename='/tmp/curses.log',level=logging.DEBUG)


class TestBoardClass(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_defaultState(self):
        self.board.setDefaultBoardState()
        correctState = [9999,0,0,-2,0,0,0,0,5,0,3,0,0,0,-5,5,0,0,0,-3,0,-5,0,0,0,0,2,0,0,-9999]
        gameOver = self.board.gameIsOver()
        self.assertFalse(gameOver)
        self.assertEqual(self.board.board, correctState)

    def test_initialPipCount(self):
        self.board.setDefaultBoardState()
        pipCount = self.board.getPipCount()
        self.assertEqual(pipCount, {'1': 167, '-1': 167})

    def test_interMediatePipCount(self):
        initialState = [9999,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        pipCount = self.board.getPipCount()
        self.assertEqual(pipCount, {'1': 2, '-1': 24})

    def test_gameOver(self):
        initialState = [9999,0,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-15,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        pipCount = self.board.getPipCount()
        gameOver = self.board.gameIsOver()
        self.assertEqual(pipCount, {'1': 0, '-1': 15})
        self.assertTrue(gameOver)
        self.assertIn('Player 1 is the winner!', self.board.errors)

    def test_putPieceInJail(self):
        initialState = [9999,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-9999]
        finalState = [9999,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([1,2])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1,2,1)
        self.assertEqual(self.board.errors,[])
        self.assertEqual(self.board.board,finalState)

    def test_illegalMoveOppPieces(self):
        initialState = [9999,0,0,-2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([1,2])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1,2,1)
        self.assertEqual(self.board.board,initialState)
        self.assertEqual(self.board.errors, ['2 or more opposing pieces at new position'])

    def test_noPieceAtOldPosition(self):
        initialState = [9999,0,0,-2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([1,2])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1,12,11)
        self.assertEqual(self.board.board,initialState)
        self.assertIn('No pieces at old position', self.board.errors )

    def test_illegalPipError(self):
        initialState = [9999,0,0,-2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([1,2])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1,222,222)
        self.assertEqual(self.board.board,initialState)
        self.assertIn('Illegal pip error', self.board.errors )

    def test_mustGoOutOfJailFirst(self):
        initialState = [9999,1,0,-2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([1,2])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1,2,1)
        self.assertEqual(self.board.board,initialState)
        self.assertIn('you must move out of jail first', self.board.errors )

    def test_cantMoveOffTillTheEnd(self):
        initialState = [9999,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,-1,0,\
                        0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([3,2])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1,2,'home')
        self.assertEqual(self.board.board,initialState)
        self.assertIn('Pieces cant be moved off until all pieces are in the '+\
                        'last 6 places for that player.', self.board.errors )

    def test_mustMoveForward(self):
        initialState = [9999,0,0,0,1,0,0,0,0,0,0,0,0,0,0,\
                        0,0,1,0,0,0,-1,0,0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([3,2])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1, 2, 3)
        self.assertEqual(self.board.board,initialState)
        self.assertIn('Pieces can only move forward', self.board.errors )

    def test_cantMoveOutOfHome(self):
        initialState = [9999,0,1,0,1,0,0,0,0,0,0,0,0,0,0,\
                        0,0,1,0,0,0,-1,0,0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([3,2])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1, 'home', 3)
        self.assertEqual(self.board.board,initialState)
        self.assertIn('Piece cant move out of home', self.board.errors )

    def test_dontHaveDiceForMove(self):
        initialState = [9999,0,0,0,1,0,0,0,0,0,0,0,0,0,0,\
                        0,0,1,0,0,0,-1,0,0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([5,5])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1, 2, 1)
        self.assertEqual(self.board.board,initialState)
        self.assertIn('Dont have dice for that move', self.board.errors )

    def test_moveOutOFJailToEmptySlot(self):
        initialState = [9999,1,0,0,1,0,0,0,0,0,0,0,0,0,0,\
                        0,0,1,0,0,0,-1,0,0,0,0,0,0,0,-9999]
        finalState = copy.deepcopy(initialState)
        finalState[1] = 0
        finalState[-4] = 1
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([1,4])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1, 'jail', 24)
        self.assertEqual(self.board.board,finalState)
        self.assertEqual([], self.board.errors )

    def test_moveOutOFJailToSinglyOccupSlot(self):
        initialState = [9999,1,0,0,1,0,0,0,0,0,0,0,0,0,0,\
                        0,0,1,0,0,0,-1,0,0,0,0,-1,0,0,-9999]
        finalState = copy.deepcopy(initialState)
        finalState[1] = 0
        finalState[-4] = 1
        finalState[-2] = -1
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([1,4])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1, 'jail', 24)
        self.assertEqual(self.board.board,finalState)
        self.assertEqual([], self.board.errors )

    def test_moveOutOFJailTODoublyOccupSlot(self):
        initialState = [9999,1,0,0,1,0,0,0,0,0,0,0,0,0,0,\
                        0,0,1,0,0,0,-1,0,0,0,0,-2,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([1,4])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1, 'jail', 24)
        self.assertEqual(self.board.board,initialState)
        self.assertIn('2 or more opposing pieces at new position', self.board.errors )

    def test_movePieceHome(self):
        for dice in [[1,4],[4,4],[3,3]]:
            initialState = [9999,0,0,0,1,0,0,0,0,0,0,0,0,0,0,\
                        0,0,0,0,0,0,0,0,0,0,0,-2,0,0,-9999]
            finalState = copy.deepcopy(initialState)
            finalState[2] = 1
            finalState[4] = 0
            self.board.clearErrors()
            self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
            logging.debug(dice)
            self.board.setDiceRoll(dice)
            self.assertEqual(self.board.board,initialState)
            self.board.movePiece(1, 2, 'home')
            self.assertEqual(self.board.board,finalState)
            self.assertEqual([], self.board.errors )

    def test_movePieceHomeDiceFail(self):
        for dice in [[2,1],[1,1]]:
            initialState = [9999,0,0,0,0,0,0,1,0,0,0,0,0,0,0,\
                        0,0,0,0,0,0,0,0,0,0,0,-2,0,0,-9999]
            self.board.clearErrors()
            self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
            self.board.setDiceRoll(dice)
            self.assertEqual(self.board.board,initialState)
            self.board.movePiece(1, 5, 'home')
            self.assertEqual(self.board.board,initialState)
            self.assertEqual([], self.board.errors )

    def test_moveToOwnSoloPiece(self):
        initialState = [9999,0,0,1,1,0,0,0,0,0,0,0,0,0,0,\
                        0,0,1,0,0,0,-1,0,0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([1,2])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1, 2, 1)
        finalState = copy.deepcopy(initialState)
        finalState[3] = 2
        finalState[4] = 0
        self.assertEqual(self.board.board,finalState)

    def test_getOutOfJailBug1(self):
        initialState = [9999, 1, 0, 0, 0, -1, 0, 0, 5, 0, \
                        3,-1,0,0,-4,4,0,0,0,-3,-1,-5,1,0,1,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState),1)
        self.board.setDiceRoll([3,5])
        self.assertEqual(self.board.board,initialState)
        self.board.movePiece(1, 'jail', 20)
        finalState = copy.deepcopy(initialState)
        finalState[1] = 0
        finalState[22] = 2
        self.assertEqual(self.board.board,finalState)

    def test_noValidMoves(self):
        initialState = [9999,1,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                        0,0,0,0,0,0,-2,-2,-2,-2,-2,-2,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([1,2])
        self.assertEqual(self.board.board,initialState)
        moveAvailable = self.board.playerHasMoveAvailable()
        self.assertFalse(moveAvailable)
        self.assertIn('2 or more opposing pieces at new position', self.board.errors )

class TestEngineClass(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_onePieceToMove(self):
        self.board.setDefaultBoardState()
        initialState = [9999,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([1,2])
        self.assertEqual(self.board.board,initialState)
        engine = BGEngine(copy.deepcopy(self.board))
        engine.addDice(copy.deepcopy(self.board.getActiveDice()))
        move = engine.getMoveForPlayer(1)
        self.assertEqual(move,[(11,9),(9,8)])

    def test_onePieceInJailPosPlayer(self):
        self.board.setDefaultBoardState()
        initialState = [9999,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([1,2])
        self.assertEqual(self.board.board,initialState)
        engine = BGEngine(copy.deepcopy(self.board))
        engine.addDice(copy.deepcopy(self.board.getActiveDice()))
        move = engine.getMoveForPlayer(1)
        self.assertEqual(move,[('jail',24),(24,22)])

    def test_onePieceInJailNegPlayer(self):
        self.board.setDefaultBoardState()
        initialState = [9999,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), -1)
        self.board.setDiceRoll([1,2])
        engine = BGEngine(copy.deepcopy(self.board))
        engine.addDice(copy.deepcopy(self.board.getActiveDice()))
        move = engine.getMoveForPlayer(-1)
        self.assertEqual(move,[('jail',1),(1,3)])
	
    def test_getMovesReturnsFalse(self):
        self.board.setDefaultBoardState()
        initialState = [9999,1,0,0,0,0,0,0,5,0,3,1,0,0,-4,4,1,0,-1,-4,-1,-5,0,0,0,0,0,0,0,-9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([2,6])
        engine = BGEngine(copy.deepcopy(self.board))
        engine.addDice(copy.deepcopy(self.board.getActiveDice()))
        move = engine.getMoveForPlayer(1)
        self.assertEqual(move,[('jail',23),(14,8)])

    def test_getMovesReturnsFalse2(self):
        self.board.setDefaultBoardState()
        initialState = [9999, -1, 1, 1, 2, 2, 4, 2, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, -4, -3, -4, -3, 0, 0, -9999]
        self.board.clearErrors()
        self.board.setCustomBoardState(copy.deepcopy(initialState), 1)
        self.board.setDiceRoll([3,6,])
        engine = BGEngine(copy.deepcopy(self.board))
        engine.addDice(copy.deepcopy(self.board.getActiveDice()))
        move = engine.getMoveForPlayer(1)
        self.assertEqual(move,[('jail',1),(1,3)])





if __name__ == '__main__':
    unittest.main()
