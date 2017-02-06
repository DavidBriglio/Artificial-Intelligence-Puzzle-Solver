import random
from datetime import datetime

class SpaceProblemGame:

    def __init__(self, w, h, spaces, newAi):
        self.width = w
        self.height = h
        self.ai = newAi
        self.spaceCount = spaces
        self.board = [[0 for x in range(w)] for y in range(h)]
        random.seed(datetime.now())
        self.setupGame()

    def setupGame(self):
        numberCount = (self.width * self.height) - self.spaceCount
        tempArray = []

        for i in range(1, numberCount + 1):
            tempArray.append(i)

        for i in range(self.spaceCount):
            tempArray.append(0)

        for colIndex in range(len(self.board)):
            for rowIndex in range(len(self.board[colIndex])):
                index = random.randint(0, len(tempArray) - 1)
                self.board[colIndex][rowIndex] = tempArray[index]
                tempArray.remove(tempArray[index])

    def makeMove(self, px, py, direction):
        if direction == "left" and px - 1 >= 0:
            self.swap(px, py, px - 1, py)
        elif direction == "right" and px + 1 <= self.width - 1:
            self.swap(px, py, px + 1, py)
        elif direction == "up" and py - 1 >= 0:
            self.swap(px, py, px, py - 1)
        elif direction == "down" and py + 1 <= self.height - 1:
            self.swap(px, py, px, py + 1)
        else:
            print("Invalid Move.")

    def swap(self, p1x, p1y, p2x, p2y):
        temp = self.board[p1y][p1x]
        self.board[p1y][p1x] = self.board[p2y][p2x]
        self.board[p2y][p2x] = temp

    def printBoard(self):
        for row in self.board:
            print(row)

    def userGameLoop(self):
        endGame = False
        while endGame == False:
            px = input("X: ")
            py = input("Y: ")
            direction = input("Direction: ")
            if px != '' and py != '' and direction != '':
                self.makeMove(int(px), int(py), direction)
            else:
                print("Invalid Input.")
            self.printBoard()

    def aiGameLoop(self):
        endGame = False
        while endGame == False:
            px, py, direction = self.ai.makeMove()
        if px != '' and py != '' and direction != '':
            self.makeMove(int(px), int(py), direction)
        else:
            print("Invalid Input.")
        self.printBoard()

if __name__ == "__main__":
    w = input("Width: ")
    l = input("Length: ")
    s = input("Spaces: ")
    game = SpaceProblemGame(w,l,s,None)
    #game = SpaceProblemGame(3,3,1,None)
    game.printBoard()
    game.userGameLoop()
    #game.aiGameLoop()
