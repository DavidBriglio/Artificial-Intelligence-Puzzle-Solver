import copy

class BfsAi:

    statesVisited = {}
    stateQueue = []
    moveList = []

    def __init__(self, game):
        self.game = game
        self.stateQueue.append(game.currentNode)
        self.solveProblem()

    def makeMove(self):
        newMove = copy.deepcopy(self.moveList[0])
        self.moveList.pop(0)
        return newMove

    def solveProblem(self):
        if self.stateQueue:
            if self.game.checkGameEnd(self.stateQueue[0]):
                print("  BFS: SOLUTION FOUND!")
                self.moveList.append(self.stateQueue[0])
                return True
            else:
                moves = self.game.expandNodes(self.stateQueue[0])
                for move in moves:
                    condensed = self.game.getCondensedNode(move)
                    if not condensed in self.statesVisited:
                        self.statesVisited[condensed] = True
                        self.stateQueue.append(move)
                    #else:
                        #Do not add it to the queue

                self.moveList.append(self.stateQueue[0])
                self.stateQueue.pop(0)

                if self.solveProblem() == False:
                    self.moveList.pop() #Remove the last item
                    return False
                else:
                    return True

        return False
