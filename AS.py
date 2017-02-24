import copy

class AsAi:

    statesVisitedOpen = set()
    statesVisitedClosed = set()
    openQueue = []
    closeSet = set()
    moveList = []

    def __init__(self, game):
        self.game = game
        self.openQueue.append(game.currentNode)
        self.currentNode = copy.deepcopy(game.currentNode)
        self.winningNode = self.solveProblem()
        print(self.winningNode)
        self.makeMoveList()

    def makeMove(self):
        return self.moveList.pop()

    def makeMoveList(self):
        node = self.winningNode
        while node != None:
            self.moveList.append(node.action)
            node = node.parent

    def solveProblemNonSlides(self):
        while self.openQueue:

            #Get lowest cost / remove it from OPEN
            self.openQueue.sort()
            nextNode = self.openQueue.pop(0)
            #print(nextNode)
            if self.game.checkGameEnd(nextNode):
                print("A* FOUND SOLUTION.")
                return nextNode

            # Get all children of best node
            nodes = self.game.expandNodes(nextNode)

            # Add node to CLOSE
            self.closeSet.add(nextNode)

            #Iterate over children
            for node in nodes:
                prevNode = None
                if node in self.openQueue:
                    prevNode = self.openQueue[self.openQueue.index(node)]
                elif node in self.closeSet:
                    setlist = list(self.closeSet)
                    prevNode = setlist[setlist.index(node)]

                #Get heuristic cost
                heuristicCost = self.game.getHeuristic(node)

                # If we have not previously generated the node
                if prevNode == None:
                    node.cost = node.depth + heuristicCost
                    self.openQueue.append(node)
                else:
                    # If the current path is less cost than the previous, update the cost and parent
                    if prevNode.cost > (node.depth + heuristicCost):
                        prevNode.depth = node.depth
                        prevNode.cost = node.depth + heuristicCost
                        prevNode.parent = nextNode
                        #TODO: Update the associated children with this node

        return None
