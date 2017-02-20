import copy

class DfsAi:

    statesVisited = set()
    stateStack = []
    moveList = []

    def __init__(self, game):
        self.game = game
        self.stateStack.append(game.currentNode)
        self.winningNode = self.solveProblem()
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
                return node
            else:
                #Add all unvisited nodes to the stack
                nodes = self.game.expandNodes(node)
                for tempNode in nodes:
                    condensed = self.game.getCondensedNode(tempNode)
                    if not condensed in self.statesVisited:
                        self.stateStack.append(tempNode)
                        self.statesVisited.add(condensed)

                        #Recurse to find the solution
                        solution = self.solveProblem()
                        if solution:
                            return solution

        return None
