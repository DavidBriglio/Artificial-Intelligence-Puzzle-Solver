import copy


class Node:

    depth = 0
    cost = 0

    def __init__(self, state, action, parent):
        self.state = copy.deepcopy(state)
        self.parent = copy.deepcopy(parent)
        self.action = copy.deepcopy(action)
        if self.parent != None:
            self.depth = copy.deepcopy(self.parent.depth + 1)
        else:
            self.depth = 0
		#self.cost = self.depth

    def __repr__(self):
        #return str(self.state) + ", " + str(self.depth) + ", " + str(self.action) + ", " + str(self.cost)
        return "State=" + str(self.state) + ", Action=" + str(self.action) + ", Depth=" + str(self.depth)

    def __str__(self):
        return "State=" + str(self.state) + ", Depth=" + str(self.depth) + ", Action=" + str(self.action) + ", Cost=" + str(self.cost)
