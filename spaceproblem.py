import random
import copy
from datetime import datetime
from node import Node

#rotate and slice: gridCopy = list(reversed(list(zip(*gridCopy[1:]))))
#NOTE: When indexing into the game board, use board[row][col]
class SpaceProblemGame:

    currentNode = None
    ai = None

    def __init__(self, w, h, spaces, newAi):
        self.ai = newAi
        board = [[0 for x in range(w)] for y in range(h)]
        random.seed(datetime.now())
        self.setupGame(board, w, h, spaces)
        self.currentNode = Node({"board":board, "spaceCount":spaces, "width":w, "height":h}, None)

    def getWinningState(self):
	    #Initialize the state
	    #state = [[0 for x in range(self.width)] for y in range(self.height)]
        return [[1,2,3],[8,0,4],[7,6,5]] #TODO: put in logic

    def setupGame(self, board, width, height, spaceCount):
        numberCount = (width * height) - spaceCount
        tempArray = []

        for i in range(1, numberCount + 1):
            tempArray.append(i)

        for i in range(spaceCount):
            tempArray.append(0)

        for colIndex in range(len(board)):
            for rowIndex in range(len(board[colIndex])):
                index = random.randint(0, len(tempArray) - 1)
                board[colIndex][rowIndex] = tempArray[index]
                tempArray.remove(tempArray[index])

    #TODO: Cleanup the speed of this, and fully implement all knight moves
    def getMovesFromPosition(self, node, row, col):

        #Boolean if the tile selected is a blank tile
        moves = []
        isBlankSpace = node.state["board"][row][col] == 0
        height = node.state["height"] - 1
        width = node.state["width"] - 1

        #left
        if col - 1 >= 0 and (node.state["board"][row][col-1] == 0 or isBlankSpace):
            moves.append(node.state["board"][row][col-1])

        #right
        if col + 1 <= width and (node.state["board"][row][col+1] == 0 or isBlankSpace):
            moves.append(node.state["board"][row][col+1])

        #up
        if row - 1 >= 0 and (node.state["board"][row-1][col] == 0 or isBlankSpace):
            moves.append(node.state["board"][row-1][col])

        #down
        if row + 1 <= height and (node.state["board"][row+1][col] == 0 or isBlankSpace):
            moves.append(node.state["board"][row+1][col])

        #up right
        if row - 1 >= 0 and col + 1 <= width and (node.state["board"][row-1][col+1] == 0 or isBlankSpace):
            moves.append(node.state["board"][row-1][col+1])

        #up left
        if col - 1 >= 0 and row - 1 >= 0 and (node.state["board"][row - 1][col - 1] == 0 or isBlankSpace):
            moves.append(node.state["board"][row-1][col-1])

        #down left
        if col - 1 >= 0 and row + 1 <= height and (node.state["board"][row+1][col-1] == 0 or isBlankSpace):
            moves.append(node.state["board"][row+1][col-1])

        #down right
        if col + 1 <= width and row + 1 <= height and (node.state["board"][row + 1][col + 1] == 0 or isBlankSpace):
            moves.append(node.state["board"][row+1][col+1])

        if not isBlankSpace:
            #knight >^
            if col + 2 <= width and row - 1 >= 0 and node.state["board"][row-1][col+2] != 0:
                moves.append(node.state["board"][row-1][col+2])

            #knight <^
            if col - 2 >= 0 and row - 1 >= 0 and node.state["board"][row-1][col-2] != 0:
                moves.append(node.state["board"][row-1][col-2])

            #knight >v
            if col + 2 <= width and row + 1 <= height and node.state["board"][row+1][col+2] != 0:
                moves.append(node.state["board"][row+1][col+2])

            #knight <v
            if col - 2 >= 0 and row + 1 <= height and node.state["board"][row+1][col-2] != 0:
                moves.append(node.state["board"][row+1][col-2])

            #knight >^
            if col + 1 <= width and row - 2 >= 0 and node.state["board"][row-2][col+1] != 0:
                moves.append(node.state["board"][row-2][col+1])

            #knight <^
            if col - 1 >= 0 and row - 2 >= 0 and node.state["board"][row-2][col-1] != 0:
                moves.append(node.state["board"][row-2][col-1])

            #knight >v
            if col + 1 <= width and row + 2 <= height and node.state["board"][row+2][col+1] != 0:
                moves.append(node.state["board"][row+2][col+1])

            #knight <v
            if col - 1 >= 0 and row + 2 <= height and node.state["board"][row+2][col-1] != 0:
                moves.append(node.state["board"][row+2][col-1])

        return moves

    def expandNodes(self, node):
        movesets = self.getMoves(node)
        nodes = []
        for moveset in movesets:            #TODO: A new board is not being used each time
            for move in moveset["moves"]:
                tempNode = copy.deepcopy(node)
                self.swap(tempNode, moveset["slot"], move)
                nodes.append(tempNode)
        return nodes

    def getMoves(self, node):
        possibleMoves = []
        for rowIndex in range(0,node.state["height"]):
            for colIndex in range(0,node.state["width"]):
                moves = self.getMovesFromPosition(node, rowIndex, colIndex)
                if moves != None:
                    possibleMoves.append({"slot":node.state["board"][rowIndex][colIndex], "moves":moves})
        return possibleMoves

    def swap(self, node, tile1, tile2):
        index1row, index1col = self.getPosition(node, tile1)
        index2row, index2col = self.getPosition(node, tile2)
        temp = node.state["board"][index1row][index1col]
        node.state["board"][index1row][index1col] = node.state["board"][index2row][index2col]
        node.state["board"][index2row][index2col] = temp

    def getPosition(self, node, tile):
        for rowIndex in range(0, node.state["height"]):
            for colIndex in range(0, node.state["width"]):
                if node.state["board"][rowIndex][colIndex] == tile:
                    return rowIndex, colIndex

    def printBoard(self, node):
        for row in node.state["board"]:
            print(row)

    def userGameLoop(self):
        endGame = False
        while endGame == False:
            px = input("X: ")
            py = input("Y: ")
            direction = input("Direction: ")
            if px != '' and py != '' and direction != '':
                self.makeMove(self.currentNode, int(px), int(py), direction)
            else:
                print("Invalid Input.")
            self.printBoard(self.currentNode)

    def aiGameLoop(self):
        endGame = False
        while endGame == False:
            px, py, direction = self.ai.makeMove()
        if px != '' and py != '' and direction != '':
            self.makeMove(self.currentNode, int(px), int(py), direction)
        else:
            print("Invalid Input.")
        self.printBoard(self.currentNode)

if __name__ == "__main__":
    #w = input("Width: ")
    #l = input("Length: ")
    #s = input("Spaces: ")
    #game = SpaceProblemGame(w,l,s,None)
    game = SpaceProblemGame(3,3,1,None)
    print("Current Board: ")
    game.printBoard(game.currentNode)
    nodes = game.expandNodes(game.currentNode)
    for node in nodes:
        print("Possible Move: ")
        print(game.printBoard(node))
    #game.userGameLoop()
    #game.aiGameLoop()
