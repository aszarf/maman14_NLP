from tree import *

# Transforms Node n in Tree t to h-level Markovization
def Markovize(t, n, h): # h - view on brothers
    pass
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
    
def children_to_tuples(children_list,h):
    new_child = Tree.Node()
    new_child.data.label = move_asterisk_right(children_list[0].parent.data.label)

    new_child.children = []
    
    if len(children_list) <= 2:
        new_child.children = children_list
    else:
        new_child.children.append(children_list[0])
        new_child.children.append(children_to_tuples(children_list[1:], h))
        for c in new_child.children:
            ApplyCNF(c, h)
    new_child.num_children = len(new_child.children)
    if len(new_child.children) > 2:
        import ipdb;ipdb.set_trace()
    return new_child
    
# Transforms grammar tree into CNF grammar tree
def ApplyCNF(t, h): # tree to CNF tree
    print t.ToString()
    # import ipdb;ipdb.set_trace()
    if hasattr(t, 'head'):
        n = t.head.children[0] # to remove 'TOP'
    else:
        n = t
    
    
    if len(n.children) > 2:
        n.data.label = "%s*%s" % (n.data.label, "-".join(map(lambda x: x.data.label.split(' ')[0], n.children)))
        children = n.children
        n.children = []
        n.children.append(children[0])
        n.children.append(children_to_tuples(children[1:], h))
        n.num_children = 2
    for c in n.children:
        ApplyCNF(c, h)

    if hasattr(t, 'head'):
        t.head.children = [n]
        print t.ToString()
        import ipdb;ipdb.set_trace()
    # print t.ToString()
    
    	
    # TODO: Copy implementation to here.
        
    return t

# Transforms CNF grammar tree into original grammar tree
def RemoveCNF(t): # CNF tree to tree

    # TODO: Implement.
    
    return t

