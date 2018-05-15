#
# Class for reading and writing tree strings and
# obtaining tree stats.
#
class Tree:

    #
    # Class for data stored in tree node
    #
    class Data:
        # Initializes empty Data
        def __init__(self):
            self.type = ''      # Type of node
            self.label = ''     # Node label
            self.dominant = ''  # Dominant node in sub-tree

    #
    # Class for tree node
    #
    class Node:
        # Initializes empty Node
        def __init__(self):
            self.num_children = 0
            self.children = []
            self.data = Tree.Data()

        # Adds Node child to node
        def AddChild(self, child):
            if not isinstance(child, Tree.Node):
                raise Exception('Can only add Node child!')
            self.children.append(child)
            self.num_children = self.num_children + 1

        # Returns string representation of sub-tree
        def ToString(self):
            res = '(' + self.data.label
            for child in self.children:
                res = res + ' ' + child.ToString()
            res = res + ')'
            return res

        # Returns True if node is leaf
        def IsLeaf(self):
            return self.num_children == 0

        # Returns sentence part the sub-tree represents
        def LeavesToString(self):
            res = ''
            if self.IsLeaf():
                label = self.data.label.split(' ')
                res = label[1]
                for i in range(2,len(label)):
                    res = res + ' ' + label[i]
                return res
            first = True
            for child in self.children:
                if not first:
                    res = res + ' '
                res = res + child.LeavesToString()
                first = False
            return res

        # Calculates count for all types of node-children
        # pairs in sub-tree
        def GramCount(self):
            res = {}
            if self.IsLeaf():
                return res
            
            head = self.data.label
            tail = []
            for child in self.children:
                tail.append(child.data.label.split(' ')[0])
                child_gram = child.GramCount()
                for pair in child_gram:
                    if not pair in res:
                        res[pair] = 0
                    res[pair] = res[pair] + child_gram[pair]

            pair = (head, tuple(tail))
            if not pair in res:
                res[pair] = 0
            res[pair] = res[pair] + 1

            return res

    # Initializes empty Tree
    def __init__(self):
        self.head = Tree.Node()
        self.__parsehelper = -1

    def next_bracket(self, s, loc):
        offset1 = s[loc:].find("(")
        offset2 = s[loc:].find(")")
        if offset1 == offset2 == -1:
            return len(s)
        else:
            if offset1 != -1 and offset2 != -1:
                return loc+min(offset1, offset2)
            else:
                return loc+max(offset1, offset2)
        
    # Returns true if string represents a valid tree
    def __IsStringValid(self, s, loc, count):
        if type(s) != str:
            return False
        if loc >= len(s):
            return count == 0
        if count < 0:
            return False
        offset_next_bracket = self.next_bracket(s, loc+1)
        if s[loc] == '(':
            return self.__IsStringValid(s, offset_next_bracket, count+1)
        elif s[loc] == ')':
            return self.__IsStringValid(s, offset_next_bracket, count-1)
        return self.__IsStringValid(s, offset_next_bracket, count)

    # Recursively parses a string into a Tree
    def __rParse(self, node, s, loc):

        # Find start of node
        while loc < len(s) and s[loc] != '(' and s[loc] != ')':
            loc = loc + 1
        if loc >= len(s) or s[loc] == ')':
            self.__parsehelper = loc
            return node

        # Find end of label
        nloc = loc + 1
        while nloc < len(s) and s[nloc] != '(' and s[nloc] != ')':
            nloc = nloc + 1

        node.data.label = s[loc+1:nloc].strip(' ')

        if s[nloc] == ')':
            self.__parsehelper = nloc
            return node
        
        while nloc < len(s):
            temp = self.__rParse(Tree.Node(), s, nloc)
            if temp.data.label != '':
                node.AddChild(temp)
            nloc = self.__parsehelper + 1
            if s[nloc] == ')':
                self.__parsehelper = nloc
                return node 
            
        return node

    # Parses a string into a matching tree
    def ParseFromString(self, s):
        if not self.__IsStringValid(s, 0, 0):
            raise Exception('Invalid tree string')

        self.head = self.__rParse(self.head, s, 0)

    # Returns a string representation of tree
    def ToString(self):
        return self.head.ToString()

    # Returns the sentence the tree represents
    def LeavesToString(self):
        return self.head.LeavesToString()

    # Returns list of leaves (lexemes)
    def GetLeaves(self):
        return self.LeavesToString().split(' ')

    # Counts each type of leaf and returns dictionary of
    # counters
    def CountLeaves(self):
        res = {}
        leaves = self.GetLeaves()
        for leaf in leaves:
            if not leaf in res:
                res[leaf] = 0
            res[leaf] = res[leaf] + 1
        return res

    # Calculates count for all types of node-children
    # pairs in tree
    def GramCount(self):
        return self.head.GramCount()
