import copy
from node import Node
from BFS import BfsAi

#TODO: Fix consistancy of tabs/spaces
class BridgeAndTorchGame:

    currentNode = None
    ai = None

    def __init__(self, newPersonSet):
        self.currentNode = Node({"bridgeSide1":newPersonSet, "bridgeSide2":[], "torchOnSide1":True}, None)

    def setAi(self, newAi):
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
        endGame = False
        while endGame == False:
            print("Asking AI for move.")
            node = self.ai.makeMove()
            if node == None:
                print("AI found no solution.")
                endGame = True
            else:
                print("AI move:")
                self.printState(node)
                endGame = self.checkGameEnd(node)
            if endGame:
                print("Game End.")

    def checkGameEnd(self, node):
        return node.state["bridgeSide1"] == []

    def expandNodes(self, node):
        options = []
        possibleNodes = []
        if node.state["torchOnSide1"]:
            options = self.getMoves(node.state["bridgeSide1"])
        else:
            options = self.getMoves(node.state["bridgeSide2"])

        for option in options:
            tempNode = copy.deepcopy(node)
            self.makeMove(tempNode, option[0], option[1])
            possibleNodes.append(tempNode)

        return possibleNodes

    def getMoves(self, side):
        options = []
        for person in side:
            options.append([person, None])
            for person2 in side:
                if person != person2:
                    options.append([person, person2])
        return options

    def printState(self, node):
        print("Side 1: " + str(node.state["bridgeSide1"]))
        print("Side 2: " + str(node.state["bridgeSide2"]))
        print("Torch on Side 1: " + str(node.state["torchOnSide1"]))

    def getCondensedNode(self, node):
        returnString = "1S"
        for person in node.state["bridgeSide1"]:
            returnString += str(person)
        returnString += "2S"
        for person in node.state["bridgeSide2"]:
            returnString += str(person)
        returnString += str(node.state["torchOnSide1"])
        return returnString

if __name__ == "__main__":
    # personLength = int(input("Number of People: "))
    # people = []
    # for index in range(personLength):
    #     person = int(input("Person " + str(index+1) + ": "))
    #     people.append(person)
    # game = BridgeAndTorchGame(people, None)
    # game.printBoard()
    game = BridgeAndTorchGame([1,2,3])
    game.setAi(BfsAi(game))
    # game.userGameLoop()
    print("Game Start.")
    game.aiGameLoop()
    # game = BridgeAndTorchGame([1,2,3,4], None)
    # nodes = game.expandNodes(game.currentNode)
    # game.printState(game.currentNode)
    # for node in nodes:
    #     game.printState(node)
    #     print()
