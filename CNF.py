from tree import *

# Transforms Node n in Tree t to h-level Markovization
def Markovize(parent, n, h):    
    if h == -1:
        return n
    
    if n.data.label.find('@') != -1:
        return n
    elif n.data.label.find(' ') != -1:
        leave = n.data.label.split(' ')[1]
        n.data.label = n.data.label.split(' ')[0]
    else:
        leave = None
        
    extension = '@'
    left_brothers = n.data.label.split('*')[0]
    if n.data.label.find('*') != -1:
        left_brothers = left_brothers.split('-')
        left_brothers = left_brothers[1:] # without parent
    else:
        left_brothers = []
    
    if len(left_brothers) > 0:
        h = min(len(left_brothers), h)
    else:
        h = min(len(parent.children)-1, h)
    
    for i in xrange(h):
        if len(left_brothers) > 0:
            extension = extension + '/' + left_brothers[::-1][i]
        else:
            # Only one brother
            extension = extension + '/' + parent.children[0].data.label.split(' ')[0]
            break

    extension = extension + '/'
    if len(extension) == 2:
        extension = extension + '/'
    n.data.label = n.data.label + extension
    
    if leave:
        n.data.label = n.data.label + ' ' + leave
    
    return n

def DeMarkovize(n):
    n.data.label = n.data.label.split('@')[0]
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
    
def build_new_child(children_list, original_parent, wanted_parent,h):
    new_child = Tree.Node()
    new_child.data.label = move_asterisk_right(wanted_parent.data.label)
    new_child.parent = wanted_parent
    
    if len(children_list) <= 2:
        new_child.children = children_list
        if len(children_list) == 2:
            if new_child.children[1].data.label.find(' ') != -1:
                leave = new_child.children[1].data.label.split(' ')[1]
            else:
                leave = None
            new_child.children[1].data.label = move_asterisk_right(new_child.data.label.split(' ')[0])
            if leave:
                new_child.children[1].data.label = new_child.children[1].data.label + ' ' + leave
    else:
        left_child = children_list[0]
        tmp = build_new_child(children_list[1:], original_parent, new_child, h)
        right_child = Markovize(original_parent, tmp, h)
        right_child = tmp
        new_child.children = [left_child, right_child]
        for c in new_child.children:
            ApplyCNF(c, h)
    new_child.num_children = len(new_child.children)

    return new_child
    
# Transforms grammar tree into CNF grammar tree
def ApplyCNF(t, h):
    if hasattr(t, 'head'):
        n = Tree.Node()
        n.data.label = t.head.data.label
        n.children = t.head.children
        n.num_children = len(t.head.children)
    else:
        n = t
        
    original_parent_t = Tree()
    original_parent_t.ParseFromString(n.ToString())
    original_parent = Tree.Node()
    original_parent.data.label = original_parent_t.head.data.label
    original_parent.children = original_parent_t.head.children
    original_parent.num_children = len(original_parent_t.head.children)
                              
    if len(n.children) == 2:
        n.children[1] = Markovize(original_parent, n.children[1], h)
    elif len(n.children) > 2:
        n.data.label = n.data.label.split('@')[0]
        n.data.label = "%s*%s" % (n.data.label, "-".join(map(lambda x: x.data.label.split(' ')[0], n.children)))
        
        left_child = n.children[0]
        tmp = build_new_child(n.children[1:], original_parent, n, h)
        right_child = Markovize(original_parent, tmp, h)
        n.children = [left_child, right_child]
        n.num_children = 2
    
    for c in n.children:
        ApplyCNF(c, h)
        
    return n

# Transforms CNF grammar tree into original grammar tree
def RemoveCNF(t):
    if hasattr(t, 'head'):
        n = Tree.Node()
        n.data.label = t.head.data.label
        n.children = t.head.children
        n.num_children = len(t.head.children)
    else:
        n = t
          
    n = DeMarkovize(n)
            
    for c in n.children:
        out = RemoveCNF(c)
        if isinstance(out, list):
            
            new_children = [n.children[0]] + out
            if len(n.data.label.split('*')[0].split('-')) == 1:
                n.children = new_children
                n.data.label = n.data.label.split('*')[0]
                return n
            else:
                return new_children
    
    if n.data.label.find('*') != -1:
        if len(n.data.label.split('*')[0].split('-')) != 1:
            return n.children
        else:
            n.data.label = n.data.label.split('*')[0]
        
    return n

