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
        self.currentNode = deepcopy(game.currentNode)
        self.winningNode = self.solveProblemNonSlides()
        self.makeMoveList()

    def makeMove(self):
        return self.moveList.pop()

    def makeMoveList(self):
        node = self.winningNode
        while node != None:
            self.moveList.append(node.action)
            node = node.parent

    def solveProblem(self):
        if self.openList:

            # Find the most optimal node
            nextNode = None
            for key, node in openList.items():
                if node.cost > nextNode.cost:
                    nextNode = node

            # Get all children of best node
            nodes = self.game.expandNodes(nextNode)

            condensed = self.game.getCondensedNode(nextNode)

            # Add node to CLOSE
            self.closeList[condensed] = nextNode

            # Remove the node from OPEN
            self.openList.pop(condensed, None)

            #Iterate over children
            for node in nodes:
                condensed = self.game.getCondensedNode(node)
                prevNode = self.openList[condensed]
                heuristicCost = self.game.getHeuristic1(node)
                if prevNode == None:
                    prevNode = self.closeList[condensed]

                # If we have not previously generated the node
                if prevNode == None:
                    node.cost = node.depth + heuristicCost
                    self.openList.append(node)
                else:
                    # If the current path is less cost than the previous, update the cost and parent
                    if prevNode.cost > (node.depth + heuristicCost):
                        prevNode.code = node.depth + heuristicCost
                        prevNode.parent = nextNode
                    #TODO: FINISH

            if self.game.checkGameEnd()
        return None


    def solveProblemNonSlides(self):
        if self.openQueue:

            #Get lowest cost / remove it from OPEN
            nextNode = self.openQueue.sort().pop(0)

            if self.game.checkGameEnd(nextNode):
                return nextNode

            # Get all children of best node
            nodes = self.game.expandNodes(nextNode)

            # Add node to CLOSE
            self.closeSet.add(nextNode)

            #Iterate over children
            for node in nodes:
                prevNode = None
                if node in openQueue:
                    prevNode = openQueue[openQueue.index(node)]
                elif node in closeSet:
                    setlist = list(closeSet)
                    prevNode = setlist[setlist.index(node)]

                # If we have not previously generated the node
                if prevNode == None:
                    node.cost = node.depth + heuristicCost
                    self.openQueue.add(node)
                else:
                    # If the current path is less cost than the previous, update the cost and parent
                    if prevNode.cost > (node.depth + heuristicCost):
                        prevNode.depth = node.depth
                        prevNode.cost = node.depth + heuristicCost
                        prevNode.parent = nextNode
                        #TODO: Update the associated children with this node

        return None
