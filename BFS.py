import copy
import queue

class BfsAi:

    statesVisited = {}
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
        #print("----")
        #Check if the queue is empty
        if self.stateQueue:

            #Pop the next state from the queue
            state = self.stateQueue.get()

            #Check if that state is a game win scenario
            if self.game.checkGameEnd(state) == True:

                #If it is a winning state, return it
                print("  BFS: SOLUTION FOUND!")
                return state
            else:

                #Get all possible moves from the current node
                moves = self.game.expandNodes(state)

                #Add each possible move that has not been seen yet to the state queue
                for move in moves:
                    condensed = self.game.getCondensedNode(move)

                    if not condensed in self.statesVisited:
                        self.statesVisited[condensed] = True

                        #Check if the state is a game win scenario before adding it to the state queue
                        if self.game.checkGameEnd(move) == True:
                            #If it is a winning state, return it
                            return move
                        else:
                            #Add the state to the state queue if it is not a win
                            self.stateQueue.put(move)
                    #else:
                        #Do not add it to the queue

            #Recursive call to continue with the next set of nodes
            return self.solveProblem()
