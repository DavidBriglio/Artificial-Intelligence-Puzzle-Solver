import random
import copy
from BFS import BfsAi
from DFS import DfsAi
from AS import AsAi
from datetime import datetime
from node import Node
from sys import setrecursionlimit

#setrecursionlimit(5000)

#rotate and slice: gridCopy = list(reversed(list(zip(*gridCopy[1:]))))
#NOTE: When indexing into the game board, use board[row][col]
class SpaceProblemGame:

    currentNode = None
    ai = None
    solution = "1,2,3,8,0,4,7,6,5" #"1,2,3,0"
    heuristic = 1

    def __init__(self, w, h, spaces, he=1):
        board = [[0 for x in range(w)] for y in range(h)]
        random.seed(datetime.now())
        self.setupGame(board, w, h, spaces)
        self.currentNode = Node(board, None, None)
        self.spaceCount = spaces
        self.width = w
        self.height = h
        self.heuristic = he

    def setAi(self, newAi):
        self.ai = newAi

    def checkGameEnd(self, node):
	    #Initialize the state
	    #state = [[0 for x in range(self.width)] for y in range(self.height)]
        return node.state == self.solution #TODO: put in logic

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
    def getHMovesFromPosition(self, node, row, col):

        #Boolean if the tile selected is a blank tile
        moves = []
        board = node.state
        if board[row][col] == 0:
            return moves
        height = self.height - 1
        width = self.width - 1
        currentTile = [row,col]

        #knight >>^
        if col + 2 <= width and row - 1 >= 0 and board[row-1][col+2]:
            moves.append([currentTile,[row-1,col+2]])

        #knight <<^
        # if col - 2 >= 0 and row - 1 >= 0 and node.state[row-1][col-2]:
        #     moves.append([currentTile,[row-1,col-2]])

        #knight >>v
        if col + 2 <= width and row + 1 <= height and board[row+1][col+2]:
            moves.append([currentTile,[row+1,col+2]])

        #knight <<v
        # if col - 2 >= 0 and row + 1 <= height and node.state[row+1][col-2]:
        #     moves.append([currentTile,[row+1,col-2]])

        #knight >^^
        if col + 1 <= width and row - 2 >= 0 and board[row-2][col+1]:
            moves.append([currentTile,[row-2,col+1]])

        #knight <^^
        if col - 1 >= 0 and row - 2 >= 0 and board[row-2][col-1]:
            moves.append([currentTile,[row-2,col-1]])

        #knight >vv
        if col + 1 <= width and row + 2 <= height and board[row+2][col+1]:
            moves.append([currentTile,[row+2,col+1]])

        #knight <vv
        if col - 1 >= 0 and row + 2 <= height and board[row+2][col-1]:
            moves.append([currentTile,[row+2,col-1]])

        return moves

    def getZeroMoves(self, node):
        moves = []
        row = None
        col = None
        currentTile = None
        height = self.height - 1
        width = self.width - 1
        board = node.state

        for rowIndex in range(0,height + 1):
            for colIndex in range(0,width + 1):
                if board[rowIndex][colIndex] == 0:
                    row = rowIndex
                    col = colIndex
                    currentTile = [row,col]
                    break
            if currentTile:
                break

        #left
        if col - 1 >= 0:
            moves.append([currentTile,[row,col-1]])

        #right
        if col + 1 <= width:
            moves.append([currentTile,[row,col+1]])

        #up
        if row - 1 >= 0:
            moves.append([currentTile,[row-1,col]])

        #down
        if row + 1 <= height:
            moves.append([currentTile,[row+1,col]])

        #up right
        if row - 1 >= 0 and col + 1 <= width:
            moves.append([currentTile,[row-1,col+1]])

        #up left
        if col - 1 >= 0 and row - 1 >= 0:
            moves.append([currentTile,[row-1,col-1]])

        #down left
        if col - 1 >= 0 and row + 1 <= height:
            moves.append([currentTile,[row+1,col-1]])

        #down right
        if col + 1 <= width and row + 1 <= height:
            moves.append([currentTile,[row+1,col+1]])

        return moves

    def expandNodes(self, node):
        movesets = self.getMoves(node)
        nodes = []
        for move in movesets:
            tempNode = copy.deepcopy(node)
            self.makeMove(tempNode, move)
            nodes.append(Node(tempNode.state, move, node))
        return nodes

    def getMoves(self, node):
        possibleMoves = []
        possibleMoves.extend(self.getZeroMoves(node))
        for rowIndex in range(0,self.height):
            for colIndex in range(0,self.width):
                possibleMoves.extend(self.getHMovesFromPosition(node, rowIndex, colIndex))
        return possibleMoves

    #TODO: Check for legality?
    def makeMove(self, node, move):
        index1row, index1col, index2row, index2col = move[0][0], move[0][1], move[1][0], move[1][1]
        temp = node.state[index1row][index1col]
        node.state[index1row][index1col] = node.state[index2row][index2col]
        node.state[index2row][index2col] = temp

    def printBoard(self, node):
        for row in node.state:
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
            action = self.ai.makeMove()
            if action == None:
                #no move
                continue
            if action[0][0] != '' and action[0][1] != '' and action[1][0] != '' and action[1][1] != '':
                self.makeMove(self.currentNode, action)
            else:
                print("Invalid Input.")
            print()
            self.printBoard(self.currentNode)
            if self.checkGameEnd(self.currentNode):
                print("GAME END!")
                endGame = True

    #Count the number of tiles that are out of place
    def getHeuristic1(self, node):
        numOff = 0
        for rowIndex in range(0,self.height):
            for colIndex in range(0,self.width):
                if node.state[rowIndex][colIndex] != self.solution[rowIndex][colIndex]:
                    numOff += 1
        return numOff

    #Sum the distance each tile is out of place
    def getHeuristic2(self, node):
        return None

    def getHeuristicAvg(self, node):
        h1 = self.getHeuristic1(node)
        h2 = self.getHeuristic2(node)
        return (h1 + h2) / 2

    def getHeuristic(self, node):
        if heuristic == 1:
            return getHeuristic1(node)
        elif heuristic == 2:
            return getHeuristic2(node)
        else:
            return getHeuristicAvg(node)


    def flatten(self, state):
        flatString = ""
        for row in state:
            for col in row:
                flatString += "," + str(col)
        return flatString[1:]

    def inflate(self, state):
        newBoard = [[0 for x in range(self.width)] for y in range(self.height)]
        tiles = state.split(',')
        row = 0
        col = 0
        for tile in tiles:
            newBoard[row][col] = tile
            col += 1
            if col > self.width - 1:
                row += 1
                col = 0
        return newBoard

if __name__ == "__main__":
    #w = input("Width: ")
    #l = input("Length: ")
    #s = input("Spaces: ")
    #game = SpaceProblemGame(w,l,s,None)
    game = SpaceProblemGame(3,3,1)

    flat = game.flatten(game.currentNode.state)
    infl = game.inflate(flat)
    print(flat)
    print(infl)

    print("Current Board: ")
    game.printBoard(game.currentNode)
    # nodes = game.expandNodes(game.currentNode)
    # for node in nodes:
    #     print("Possible Move: ")
    #     print("MOVE: " + str(node.action))
    #     print(game.printBoard(node))
    #     print()


    #game.userGameLoop()


    #game.setAi(BfsAi(game))
    #game.setAi(AsAi(game))
    game.setAi(DfsAi(game))
    game.aiGameLoop()
