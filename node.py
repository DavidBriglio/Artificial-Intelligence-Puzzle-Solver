import copy

class Node:

    depth = 0
    cost = 0

    def __init__(self, state, action, parent):
        self.state = state #copy.deepcopy(state)
        self.parent = parent #copy.deepcopy(parent)
        self.action = action #copy.deepcopy(action)
        if self.parent != None:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0
		#self.cost = self.depth

    def __eq__(self, other):
        if other:
            return str(self.state) == str(other.state)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        if other != None:
            return self.cost <= other.cost
        return False

    def __lt__(self, other):
        if other != None:
            return self.cost < other.cost
        return False

    def __ge__(self, other):
        if other != None:
            return self.cost >= other.cost
        return False

    def __gt__(self, other):
        if other != None:
            return self.cost > other.cost
        return False

    def __cmp__(self, other):
        if self.cost < other.cost:
            return -1
        elif self.cost == other.cost:
            return 0
        else:
            return 1

    def __hash__(self):
        return hash(str(self.state))

    def __repr__(self):
        #return str(self.state) + ", " + str(self.depth) + ", " + str(self.action) + ", " + str(self.cost)
        return "State=" + str(self.state) + ", Action=" + str(self.action) + ", Depth=" + str(self.depth)

    def __str__(self):
        return "State=" + str(self.state) + ", Depth=" + str(self.depth) + ", Action=" + str(self.action) + ", Cost=" + str(self.cost)
