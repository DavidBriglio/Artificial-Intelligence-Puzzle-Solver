import random
from datetime import datetime
from node import Node

#rotate and slice: gridCopy = list(reversed(list(zip(*gridCopy[1:]))))
#NOTE: When indexing into the game board, use board[y][x] NOT board[x][y].
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

    #TODO: Add knight moves
    def makeMove(self, node, px, py, direction):

        #Boolean if the tile selected is a blank tile
        isBlankSpace = node.state["board"][py][px] == 0
        height = node.state["height"]
        width = node.state["width"]

        if direction == "left" and px - 1 >= 0 and (node.state["board"][py][px - 1] == 0 or isBlankSpace):
            self.swap(node, px, py, px - 1, py)
        elif direction == "right" and px + 1 <= width - 1 and (node.state["board"][py][px + 1] == 0 or isBlankSpace):
            self.swap(node, px, py, px + 1, py)
        elif direction == "up" and py - 1 >= 0 and (node.state["board"][py - 1][px] == 0 or isBlankSpace):
            self.swap(node, px, py, px, py - 1)
        elif direction == "down" and py + 1 <= height - 1 and (node.state["board"][py + 1][px] == 0 or isBlankSpace):
            self.swap(node, px, py, px, py + 1)
        elif direction == "upright" and px + 1 <= width and py - 1 >= 0 and (node.state["board"][py - 1][px + 1] == 0 or isBlankSpace):
            self.swap(node, px, py, px + 1, py - 1)
        elif direction == "upleft" and px - 1 >= 0 and py - 1 >= 0 and (node.state["board"][py - 1][px - 1] == 0 or isBlankSpace):
            self.swap(node, px, py, px - 1, py - 1)
        elif direction == "downleft" and px - 1 >= 0 and py + 1 <= height and (node.state["board"][py + 1][px - 1] == 0 or isBlankSpace):
            self.swap(node, px, py, px - 1, py + 1)
        elif direction == "downright" and px + 1 <= width and py + 1 <= height and (node.state["board"][py + 1][px + 1] == 0 or isBlankSpace):
            self.swap(node, px, py, px + 1, py + 1)
        else:
            print("Invalid Move.")

    def swap(self, node, p1x, p1y, p2x, p2y):
        temp = node.state["board"][p1y][p1x]
        node.state["board"][p1y][p1x] = node.state["board"][p2y][p2x]
        node.state["board"][p2y][p2x] = temp

    def printBoard(self):
        for row in self.currentNode.state["board"]:
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
            self.printBoard()

    def aiGameLoop(self):
        endGame = False
        while endGame == False:
            px, py, direction = self.ai.makeMove()
        if px != '' and py != '' and direction != '':
            self.makeMove(self.currentNode, int(px), int(py), direction)
        else:
            print("Invalid Input.")
        self.printBoard()

if __name__ == "__main__":
    #w = input("Width: ")
    #l = input("Length: ")
    #s = input("Spaces: ")
    #game = SpaceProblemGame(w,l,s,None)
    game = SpaceProblemGame(3,3,1,None)
    game.printBoard()
    game.userGameLoop()
    #game.aiGameLoop()
