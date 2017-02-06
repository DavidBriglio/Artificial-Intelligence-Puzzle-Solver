from node import Node

class BridgeAndTorchGame:

	bridgeSide1 = []
	bridgeSide2 = []
	torchOnSide1 = True
	ai = None

	def __init__(self, newPersonSet, newAi):
		self.bridgeSide1 = newPersonSet
		self.ai = newAi

	def makeMove(self, person1, person2):
		side = self.bridgeSide1 if self.torchOnSide1 else self.bridgeSide2
		side2 = self.bridgeSide2 if self.torchOnSide1 else self.bridgeSide1
		moveMade = False
		if person1 != None and person1 != '' and person1 in side:
			side2.append(person1)
			side.remove(person1)
			moveMade = True

		if person2 != None and person2 != '' and person2 in side:
			side2.append(person2)
			side.remove(person2)
			moveMade = True

		if moveMade == True:
			self.torchOnSide1 = self.torchOnSide1 == False

		self.bridgeSide1 = side if self.torchOnSide1 else side2
		self.bridgeSide2 = side2 if self.torchOnSide1 else side

	def printBoard(self):
		print("Side1: " + str(self.bridgeSide1))
		print("Side2: " + str(self.bridgeSide2))

	def userGameLoop(self):
		endGame = False
		while endGame == False:
			p1 = input("Move Person 1: ")
			if p1 == '':
				p1 = -1
			else:
				p1 = int(p1)

			p2 = input("Move Person 2: ")
			if p2 == '':
				p2 = -1
			else:
				p2 = int(p2)

			self.makeMove(p1, p2)
			self.printBoard()
			endGame = self.checkGameEnd()
			if endGame:
				print("Game End")

	def aiGameLoop(self):
		endGame = True
		while endGame == False:
			m1, m2 = self.ai.getMove()
			self.makeMove(m1, m2)
			self.printBoard()
			endGame = self.checkGameEnd()
			if endGame:
				print("Game End")

	def checkGameEnd(self):
		return self.bridgeSide1 == []

	def getExpand(self, node):
		options = []
		possibleNodes = []
		if self.torchOnSide1:
			options = self.getCombinations(self.bridgeSide1)
		else:
			options = self.getCombinations(self.bridgeSide2)

		#TODO: FIX - This is not the state
		for option in options:
			possibleNodes.append(Node(option, node))

		return possibleNodes

	def getCombinations(self, side):
		options = []
		for person in side:
			for person2 in side:
				if person != person2:
					options.append([person, person2])
		return options



if __name__ == "__main__":
	# personLength = int(input("Number of People: "))
	# people = []
	# for index in range(personLength):
	# 	person = int(input("Person " + str(index+1) + ": "))
	# 	people.append(person)
	# game = BridgeAndTorchGame(people, None)
	# game.printBoard()
	# #game = BridgeAndTorchGame([1,2,3], None)
	# game.userGameLoop()
	# #game.aiGameLoop()
	game = BridgeAndTorchGame([1,2,3,4], None)
	print(game.getExpand(Node([1,2,3,4], None)))
