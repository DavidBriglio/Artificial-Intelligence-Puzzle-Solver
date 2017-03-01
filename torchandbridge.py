import copy
import math
from node import Node
from BFS import BfsAi
from DFS import DfsAi
from AS import AsAi

class BridgeAndTorchGame:

    currentNode = None
    ai = None
    heuristic = 1

    def __init__(self, newPersonSet, he=1):
        self.currentNode = Node({"bridgeSide1":newPersonSet, "bridgeSide2":[], "torchOnSide1":True}, None, None)
        self.heuristic = he

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

        if moveMade:
            node.state["torchOnSide1"] = node.state["torchOnSide1"] == False

    def aiGameLoop(self):
        endGame = False
        while endGame == False:
            print("\nAsking AI for move.")
            move = self.ai.makeMove()
            if move != None:
                print("AI move:")
                print("MOVE: " + str(move))
                self.makeMove(self.currentNode, move[0], move[1])
                print("BOARD:")
                self.printState(self.currentNode)
                endGame = self.checkGameEnd(self.currentNode)
            if endGame:
                print()
                print("Game End.")

    def checkGameEnd(self, node):
        return node.state["bridgeSide1"] == []

    def expandNodes(self, node):
        options = []
        possibleNodes = []
        node.state["bridgeSide1"].sort()
        node.state["bridgeSide2"].sort()
        if node.state["torchOnSide1"] == True:
            options = self.getMoves(node.state["bridgeSide1"])
        else:
            options = self.getMoves(node.state["bridgeSide2"])

        for option in options:
            tempNode = copy.deepcopy(node)
            self.makeMove(tempNode, option[0], option[1])
            tempNode.state["bridgeSide1"].sort()
            tempNode.state["bridgeSide2"].sort()
            possibleNodes.append(Node(tempNode.state, option, node))

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

    # Returns the total number of people on side 1 (total - side 2)
    def getHeuristic1(self, node):
        return len(node.state["bridgeSide1"])

    # Returns the total speed of everyone on side 1 (total - side 2)
    def getHeuristic2(self, node):
        return sum(node.state["bridgeSide1"])

    # Get the average of the two heuristics
    def getHeuristicAvg(self, node):
        h1 = self.getHeuristic1(node)
        h2 = self.getHeuristic2(node)
        return math.floor((h1 + h2) / 2)

    def getHeuristic(self, node):
        if self.heuristic == 1:
            return self.getHeuristic1(node)
        elif self.heuristic == 2:
            return self.getHeuristic2(node)
        else:
            return self.getHeuristicAvg(node)


if __name__ == "__main__":
    side = input("Input People: ")
    ai = input("AI: ")
    he = 1
    if ai == "as":
        he = input("Heuristic: ")
    game = BridgeAndTorchGame([int(n) for n in side.split(",")], int(he))

    print()
    print("Current Board: ")
    game.printState(game.currentNode)
    print()

    if ai == "bfs":
        game.setAi(BfsAi(game))
        game.aiGameLoop()
    elif ai == "dfs":
        game.setAi(DfsAi(game))
        game.aiGameLoop()
    elif ai == "as":
        game.setAi(AsAi(game))
        game.aiGameLoop()
    else:
        game.userGameLoop()
