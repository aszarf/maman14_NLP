from tree import *

# Transforms Node n in Tree t to h-level Markovization
# def Markovize(t, n, h): # h - view on brothers
def Markovize(n, h):
    
    # TODO: Implement. May change params if necessary.

    return n

def DeMarkovize(t, n, h): # h - view on brothers

    # TODO: Implement. May change params if necessary.

    return n

def move_asterisk_right(label):
    l = label.split('-')
    res = ''
    for i in l:
        if i.find('*') == -1:
            res = res + i + '-'
        else:
            res = res + i.split('*')[0] + '-' + i.split('*')[1] + '*'
    
    return res[:-1]
    
def children_to_tuples(children_list,wanted_parent,h):
    new_child = Tree.Node()
    new_child.data.label = move_asterisk_right(wanted_parent.data.label)
    new_child.children = []
    
    if len(children_list) <= 2:
        new_child.children = children_list
    else:
        left_child = Markovize(children_list[0], h)
        right_child = Markovize(children_to_tuples(children_list[1:],new_child, h), h)
        new_child.children = [left_child, right_child]
        for c in new_child.children:
            ApplyCNF(c, h)
    new_child.num_children = len(new_child.children)

    return new_child
    
# Transforms grammar tree into CNF grammar tree
def ApplyCNF(t, h):
    if hasattr(t, 'head'):
        n = t.head.children[0] # to remove 'TOP'
    else:
        n = t
    
    if len(n.children) > 2:
        n.data.label = "%s*%s" % (n.data.label, "-".join(map(lambda x: x.data.label.split(' ')[0], n.children)))
        children = n.children
        n.children = []
        
        left_child = Markovize(children[0], h)
        right_child = Markovize(children_to_tuples(children[1:],children[1].parent, h), h)
        n.children = [left_child, right_child]
        n.num_children = 2
    for c in n.children:
        ApplyCNF(c, h)

    if hasattr(t, 'head'):
        t.head.children = [n]
        
    return t

# Transforms CNF grammar tree into original grammar tree
def RemoveCNF(t): # CNF tree to tree

    # TODO: Implement.
    
    return t

