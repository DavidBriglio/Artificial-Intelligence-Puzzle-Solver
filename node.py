import copy


class Node:

    depth = 0
    action = None
    cost = 0

    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        if self.parent != None:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0
		#self.cost = self.depth

    def __repr__(self):
        #return str(self.state) + ", " + str(self.depth) + ", " + str(self.action) + ", " + str(self.cost)
        return "State=" + str(self.state) + " Depth=" + str(self.depth)

    def __str__(self):
        return "State=" + str(self.state) + ", Depth=" + str(self.depth) + ", Action=" + str(self.action) + ", Cost=" + str(self.cost)
