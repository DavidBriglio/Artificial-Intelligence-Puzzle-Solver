import random
import copy
import math
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
        self.width = w
        self.height = h
        board = []
        random.seed(datetime.now())
        self.setupGame(board, w, h, spaces)
        self.currentNode = Node(self.flatten(board), None, None)
        self.spaceCount = spaces
        self.heuristic = he

    def setAi(self, newAi):
        self.ai = newAi

    def checkGameEnd(self, node):
	    #Initialize the state
	    #state = [[0 for x in range(self.width)] for y in range(self.height)]
        return node.state == self.solution #TODO: put in logic

    def setupGame(self, board, width, height, spaceCount):
        for i in range(1, width * height):
            board.append(str(i))

        for i in range(spaceCount):
            board.append(str(0))

        random.shuffle(board)

    def getHMovesFromPosition(self, node, index):

        #Boolean if the tile selected is a blank tile
        moves = []
        board = self.inflate(node.state)
        if board[index] == '0':
            return moves
        height = self.height - 1
        width = self.width - 1
        col, row = self.indexToPoint(index)

        #knight >>^
        otherIndex = self.pointToIndex(row-1,col+2)
        if col + 2 <= width and row - 1 >= 0 and board[otherIndex] != '0':
            moves.append([index,otherIndex])

        #knight <<^
        # otherIndex = self.pointToIndex(row-1,col-2)
        # if col - 2 >= 0 and row - 1 >= 0 and board[otherIndex] != '0':
        #     moves.append([index,otherIndex])

        #knight >>v
        otherIndex = self.pointToIndex(row+1,col+2)
        if col + 2 <= width and row + 1 <= height and board[otherIndex] != '0':
            moves.append([index,otherIndex])

        #knight <<v
        # otherIndex = self.pointToIndex(row+1,col-2)
        # if col - 2 >= 0 and row + 1 <= height and node.state[otherIndex] != '0':
        #     moves.append([index,otherIndex)

        #knight >^^
        otherIndex = self.pointToIndex(row-2,col+1)
        if col + 1 <= width and row - 2 >= 0 and board[otherIndex] != '0':
            moves.append([index,otherIndex])

        #knight <^^
        otherIndex = self.pointToIndex(row-2,col-1)
        if col - 1 >= 0 and row - 2 >= 0 and board[otherIndex] != '0':
            moves.append([index,otherIndex])

        #knight >vv
        otherIndex = self.pointToIndex(row+2,col+1)
        if col + 1 <= width and row + 2 <= height and board[otherIndex] != '0':
            moves.append([index,otherIndex])

        #knight <vv
        otherIndex = self.pointToIndex(row+2,col-1)
        if col - 1 >= 0 and row + 2 <= height and board[otherIndex] != '0':
            moves.append([index,otherIndex])

        return moves

    def getZeroMoves(self, node):
        moves = []
        height = self.height - 1
        width = self.width - 1
        board = self.inflate(node.state)
        zeros = []
        for index in range(0, len(board)):
            if board[index] == '0':
                zeros.append(index)

        for index in zeros:
            col, row = self.indexToPoint(index)
            #left
            if col - 1 >= 0:
                moves.append([index,self.pointToIndex(row,col-1)])

            #right
            if col + 1 <= width:
                moves.append([index,self.pointToIndex(row,col+1)])

            #up
            if row - 1 >= 0:
                moves.append([index,self.pointToIndex(row-1,col)])

            #down
            if row + 1 <= height:
                moves.append([index,self.pointToIndex(row+1,col)])

            #up right
            if row - 1 >= 0 and col + 1 <= width:
                moves.append([index,self.pointToIndex(row-1,col+1)])

            #up left
            if col - 1 >= 0 and row - 1 >= 0:
                moves.append([index,self.pointToIndex(row-1,col-1)])

            #down left
            if col - 1 >= 0 and row + 1 <= height:
                moves.append([index,self.pointToIndex(row+1,col-1)])

            #down right
            if col + 1 <= width and row + 1 <= height:
                moves.append([index,self.pointToIndex(row+1,col+1)])

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
        board = self.inflate(node.state)
        for index in range(0,len(board)):
            possibleMoves.extend(self.getHMovesFromPosition(node,index))
        return possibleMoves

    #TODO: Check for legality?
    def makeMove(self, node, move):
        index1, index2 = move[0], move[1]
        board = self.inflate(node.state)
        temp = board[index1]
        board[index1] = board[index2]
        board[index2] = temp
        node.state = self.flatten(board)

    def printBoard(self, node):
        board = self.inflate(node.state)
        line = ""
        count = 0
        for index in range(0, len(board)):
            line += str(board[index]) + " "
            count += 1
            if count == self.width:
                print(line)
                line = ""
                count = 0
        print()

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
            if action[0] != '' and action[1] != '':
                self.makeMove(self.currentNode, action)
            else:
                print("Invalid Input.")
            print()
            print("Move: " + str(self.indexToPoint(action[0])) + " - " + str(self.indexToPoint(action[1])))
            self.printBoard(self.currentNode)
            if self.checkGameEnd(self.currentNode):
                print("GAME END!")
                endGame = True

    #Count the number of tiles that are out of place
    def getHeuristic1(self, node):
        numOff = 0
        board = self.inflate(node.state)
        for index in range(0,len(board)):
            if board[index] != self.solution[index]:
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
        for tile in state:
                flatString += "," + str(tile)
        return flatString[1:]

    def inflate(self, state):
        return state.split(",")

    def pointToIndex(self, row, col):
        return (row * self.width) + col

    #Returns COL, ROW
    def indexToPoint(self, index):
        return (index % self.width), math.floor(index / self.width)

if __name__ == "__main__":
    #w = input("Width: ")
    #l = input("Length: ")
    #s = input("Spaces: ")
    #game = SpaceProblemGame(w,l,s,None)
    game = SpaceProblemGame(3,3,1)
    index = game.pointToIndex(2,1)
    # print(index)
    # print(game.indexToPoint(index))

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
