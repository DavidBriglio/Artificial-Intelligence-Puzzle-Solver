import copy
import queue

#TODO: utilize new __eq__ and __cmp__ in node to remove "condensed"
class BfsAi:

    statesVisited = set()
    stateQueue = queue.Queue()
    moveList = []

    def __init__(self, game):
        self.game = game
        self.stateQueue.put(game.currentNode)
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

        while self.stateQueue:
            # Pop the next state from the queue
            state = self.stateQueue.get()

            # Check if that state is a game win scenario
            if self.game.checkGameEnd(state) == True:

                # If it is a winning state, return it
                print("  BFS: SOLUTION FOUND!")
                return state
            else:

                # Get all possible moves from the current node
                moves = self.game.expandNodes(state)

                # Add each possible move that has not been seen yet to the state queue
                for move in moves:
                    condensed = self.game.getCondensedNode(move)

                    if not condensed in self.statesVisited:
                        self.statesVisited.add(condensed)
                        self.stateQueue.put(move)
