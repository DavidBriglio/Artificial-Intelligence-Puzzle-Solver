import copy
import queue

class BfsAi:

    statesVisited = {}
    stateQueue = queue.Queue()
    moveList = []

    def __init__(self, game):
        self.game = game
        self.stateQueue.put(game.currentNode)
        self.solveProblem()
        self.moveList.pop(0)
        print(self.moveList)

    def makeMove(self):
        newMove = copy.deepcopy(self.moveList[0])
        self.moveList.pop()
        return newMove.action

    def solveProblem(self):
        #print("STATE QUEUE: " + str(self.stateQueue) + "\n")
        #print("MOVE LIST: " + str(self.moveList) + "\n")

        #Check if the queue is empty
        if self.stateQueue:

            #Pop the next state from the queue
            state = self.stateQueue.get()

            #Check if that state is a game win scenario
            if self.game.checkGameEnd(state) == True:

                #Add the move to the move list, and return True
                print("  BFS: SOLUTION FOUND!")
                self.moveList.append(state)
                return True
            else:

                #Get all possible moves from the current node
                moves = self.game.expandNodes(state)

                #Add each possible move that has not been seen yet, to the state queue
                for move in moves:
                    condensed = self.game.getCondensedNode(move)
                    if not condensed in self.statesVisited:
                        #print(condensed)
                        self.statesVisited[condensed] = True

                        #Check if the state is a game win scenario before adding it to the state queue
                        if self.game.checkGameEnd(move) == True:
                            #Add it to the move list and return True if it is a win
                            self.moveList.append(move)
                            return True
                        else:
                            #Add the state to the state queue if it is not a win
                            self.stateQueue.put(move)
                    #else:
                        #Do not add it to the queue

                #Recursive call to continue with the next set of nodes
                if self.solveProblem() == False:
                    #If the game has not been solved in this path
                    self.moveList.pop() #Remove the last move
                    return False
                else:
                    #If the path is a winning path, add the current node to the move list and return True
                    self.moveList.append(state)
                    return True

        #The state queue is empty
        return False
