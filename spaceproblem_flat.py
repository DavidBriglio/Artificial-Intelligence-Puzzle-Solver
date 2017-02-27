import random
import copy
import math
from BFS import BfsAi
from DFS import DfsAi
from AS import AsAi
from datetime import datetime
from node import Node
from sys import setrecursionlimit

#rotate and slice: gridCopy = list(reversed(list(zip(*gridCopy[1:]))))
#NOTE: When indexing into the game board, use board[row][col]
class SpaceProblemGame:

    currentNode = None
    ai = None
    heuristic = 1
    tileList = []

    def __init__(self, w, h, spaces, solution, he=1):
        self.width = w
        self.height = h
        board = []
        random.seed(datetime.now())
        self.setupGame(board, w, h, spaces)
        self.currentNode = Node(self.flatten(board), None, None)
        #self.currentNode = Node(self.flatten([1,2,3,0,4,8,7,6,5]), None, None)
        self.spaceCount = spaces
        self.heuristic = he
        self.solution = solution

    def setAi(self, newAi):
        self.ai = newAi

    def checkGameEnd(self, node):
        return node.state == self.solution

    def setupGame(self, board, width, height, spaceCount):
        for i in range(1, (width * height) - spaceCount + 1):
            board.append(str(i))

        for i in range(spaceCount):
            board.append(str(0))

        self.tileList = copy.deepcopy(board)
        random.shuffle(board)

    def getHMovesFromPosition(self, node, moves):
        board = self.inflate(node.state)
        height = self.height - 1
        width = self.width - 1

        for index in range(0,len(board)):
            #Check if the current tile is blank
            if board[index] == '0':
                continue
            col, row = self.indexToPoint(index)

            #knight >>^
            otherIndex = self.pointToIndex(row-1,col+2)
            if col + 2 <= width and row - 1 >= 0 and board[otherIndex] != '0' and not [index,otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #knight <<^
            otherIndex = self.pointToIndex(row-1,col-2)
            if col - 2 >= 0 and row - 1 >= 0 and board[otherIndex] != '0' and not [index,otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #knight >>v
            otherIndex = self.pointToIndex(row+1,col+2)
            if col + 2 <= width and row + 1 <= height and board[otherIndex] != '0' and not [index,otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #knight <<v
            otherIndex = self.pointToIndex(row+1,col-2)
            if col - 2 >= 0 and row + 1 <= height and board[otherIndex] != '0' and not [index,otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #knight >^^
            otherIndex = self.pointToIndex(row-2,col+1)
            if col + 1 <= width and row - 2 >= 0 and board[otherIndex] != '0' and not [index,otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #knight <^^
            otherIndex = self.pointToIndex(row-2,col-1)
            if col - 1 >= 0 and row - 2 >= 0 and board[otherIndex] != '0' and not [index,otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #knight >vv
            otherIndex = self.pointToIndex(row+2,col+1)
            if col + 1 <= width and row + 2 <= height and board[otherIndex] != '0' and not [index,otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #knight <vv
            otherIndex = self.pointToIndex(row+2,col-1)
            if col - 1 >= 0 and row + 2 <= height and board[otherIndex] != '0' and not [index,otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

    def getZeroMoves(self, node, moves):
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
            otherIndex = self.pointToIndex(row,col-1)
            if col - 1 >= 0 and not [index, otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #right
            otherIndex = self.pointToIndex(row,col+1)
            if col + 1 <= width and not [index, otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #up
            otherIndex = self.pointToIndex(row-1,col)
            if row - 1 >= 0 and not [index, otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #down
            otherIndex = self.pointToIndex(row+1,col)
            if row + 1 <= height and not [index, otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #up right
            otherIndex = self.pointToIndex(row-1,col+1)
            if row - 1 >= 0 and col + 1 <= width and not [index, otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #up left
            otherIndex = self.pointToIndex(row-1,col-1)
            if col - 1 >= 0 and row - 1 >= 0 and not [index, otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #down left
            otherIndex = self.pointToIndex(row+1,col-1)
            if col - 1 >= 0 and row + 1 <= height and not [index, otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

            #down right
            otherIndex = self.pointToIndex(row+1,col+1)
            if col + 1 <= width and row + 1 <= height and not [index, otherIndex] in moves and not [otherIndex, index] in moves:
                moves.append([index,otherIndex])

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
        self.getZeroMoves(node, possibleMoves)
        self.getHMovesFromPosition(node, possibleMoves)
        return possibleMoves

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

    # Count the number of tiles that are out of place
    def getHeuristic1(self, node):
        numOff = 0
        board = self.inflate(node.state)
        solution = self.inflate(self.solution)
        for index in range(0,len(board)):
            if board[index] != solution[index]:
                numOff += 1
        return numOff

    # Get the distance each tile is off
    def getHeuristic2(self, node):
        board = self.inflate(node.state)
        solution = self.inflate(self.solution)
        value = 0
        for index in range(0,len(board)):
            print(index)
            if board[index] != solution[index]:
                realIndex = solution.index(board[index])
                value += abs(realIndex - index)
        return value

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
    w = input("Width: ")
    l = input("Length: ")
    s = input("Spaces: ")
    sol = input("Solution: ")
    ai = input("AI: ")
    if ai == "as":
        he = input("Heuristic: ")
    game = SpaceProblemGame(int(w),int(l),int(s),sol,int(he))
    # game = SpaceProblemGame(3,3,1,"1,2,3,8,0,4,7,6,5",2)

    print()
    print("Current Board: ")
    game.printBoard(game.currentNode)
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
