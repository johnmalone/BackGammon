class Pip () :

	def __init__(self):
		self.pieces = []

	def addPieceToPip(self, piece) :
		# shouldnt happen
		if not self.canAcceptPiece(piece) :
			return False

		# pip is either empty, one opposition or pieces type
		if not self.pieces :
			self.pieces.append(piece)
			return True

		if self.pieces[0].getPlayer() == piece.getPlayer():
			self.pieces.append(piece)
			return True

		pieceToRemove = self.pieces.pop()
		self.pieces.append(piece)
		return pieceToRemove

	def popPiece(self) :
		if not self.pieces :
			return False

		return self.pieces.pop()

	def getPipCount(self) :
		if not self.pieces :
			return 0

		return len(self.pieces)

	def getPlayerOnPip(self) :
		if not self.pieces :
			return self.pieces

		return self.pieces[0].getPlayer()

	def canAcceptPiece(self,piece) :
		if not self.pieces :
			return True

		if len(self.pieces) > 1 and \
			self.pieces[0].getPlayer() != piece.getPlayer() :
			return False

		return True

