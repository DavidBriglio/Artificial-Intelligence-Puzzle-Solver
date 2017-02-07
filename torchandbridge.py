from node import Node
#TODO: Fix consistancy of tabs/spaces
class BridgeAndTorchGame:

    currentNode = None
    ai = None
    
	def __init__(self, newPersonSet, newAi):
		self.currentNode = Node({"bridgeSide1":newPersonSet, "bridgeSide2":[], "torchOnSide1":True}, None)
		self.ai = newAi

	def makeMove(self, node, person1, person2):
		side = node.state["bridgeSide1"] if node.state["torchOnSide1"] else node.state["bridgeSide2"]
		side2 = node.state["bridgeSide2"] if node.state["torchOnSide1"] else node.state["bridgeSide1"]
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
			node.state["torchOnSide1"] = node.state["torchOnSide1"] == False

		node.state["bridgeSide1"] = side if node.state["torchOnSide1"] else side2
		node.state["bridgeSide2"] = side2 if node.state["torchOnSide1"] else side
		return node

	def printBoard(self):
		print("Current Node: " + str(self.currentNode))

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

			self.makeMove(self.currentNode, p1, p2)
			self.printBoard()
			endGame = self.checkGameEnd()
			if endGame:
				print("Game End")

	def aiGameLoop(self):
		endGame = True
		while endGame == False:
			m1, m2 = self.ai.getMove()
			self.makeMove(self.currentNode, m1, m2)
			self.printBoard()
			endGame = self.checkGameEnd()
			if endGame:
				print("Game End")

	def checkGameEnd(self):
		return self.bridgeSide1 == []

	def getExpand(self, node):
		options = []
		possibleNodes = []
		if node.state["torchOnSide1"]:
			options = self.getCombinations(node.state["bridgeSide1"])
		else:
			options = self.getCombinations(node.state["bridgeSide2"])

		#TODO: FIX v
		for option in options:
			possibleNodes.append(Node(self.makeMoveOnNode(node, option[0], option[1]), node))

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
	print(game.getExpand(Node({"bridgeSide1":[1,2,3,4], "bridgeSide2":[], "torchOnSide1":True}, None)))
