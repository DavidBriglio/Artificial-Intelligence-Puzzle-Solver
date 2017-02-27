import copy
import datetime

class DfsAi:

    statesVisited = set()
    stateStack = []
    moveList = []

    def __init__(self, game):
        print("DFS SEARCH")
        self.game = game
        self.stateStack.append(game.currentNode)
        print(datetime.datetime.now().time())
        self.winningNode = self.solveProblem()
        print(datetime.datetime.now().time())
        if self.winningNode == None:
            print("DFS DID NOT FIND A SOLUTION")
        self.makeMoveList()

    def makeMove(self):
        return self.moveList.pop()

    def makeMoveList(self):
        node = self.winningNode
        while node != None:
            self.moveList.append(node.action)
            node = node.parent

    def solveProblem(self):
        if self.stateStack:
            #Get the next node on the stack
            node = self.stateStack.pop()

            if node.depth >= 30:
                #Do not continue past depth 30
                #print("MAX REACHED")
                return None

            if self.game.checkGameEnd(node):
                #Solution found!
                print("DFS FOUND A SOLUTION!")
                return node
            else:
                # Add all unvisited nodes to the stack
                nodes = self.game.expandNodes(node)

                for tempNode in nodes:
                    if not tempNode in self.statesVisited:
                        self.stateStack.append(tempNode)
                        self.statesVisited.add(tempNode)

                        #Recurse to find the solution
                        solution = self.solveProblem()
                        if solution:
                            return solution
        return None
