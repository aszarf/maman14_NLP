# CYK Functions
from tree import *
from CNF import *
import math
import time
import timelog
import itertools

# Retrieves original tag for CNF node
def Unmask(tag, to_left):
    res = tag
    parts = tag.split('*')
    if len(parts) == 1:
        return res
    left_parts = parts[0].split('-')
    right_parts = parts[1].split('-')
    if to_left:
        res = left_parts[len(left_parts)-1]
    else:
        res = right_parts[0]
    return res

# Adds productions and unary meta-productions to CYK tables
def AddToCYK(CYK, BP, S, gram, i, s, j, tag, u_tag, P23):
    tm0 = time.time()
    # Create list of producers of tag in its masked and
    # unmasked forms.
    pre_list = {}
    if tag in gram[1]:
        set1 = gram[1][tag]
        pre_list = set1.copy()
    if u_tag in gram[1] and not tag == u_tag:
        set2 = gram[1][u_tag]
        pre_list.update(set2)
        if tag in gram[1]:
            for pre in set(set1.keys()) & set(set2.keys()):
                pre_list[pre] = set1[pre]+set2[pre]
    tm1 = time.time()
    # Add probs for producers and relevant unary
    # productions  
    for X in pre_list:
        P = pre_list[X] + P23
        if X in CYK[i][j]:
            if P > CYK[i][j][X]:
                CYK[i][j][X] = P
                BP[i][j][X] = tag
                S[i][j][X] = s
        else:
            CYK[i][j][X] = P
            BP[i][j][X] = tag
            S[i][j][X] = s
        unary = tuple(X)
        u_unary = tuple(Unmask(X, True))
        if unary in gram[1] and not unary in CYK[i][j]:
            (CYK,BP,S) = AddToCYK(CYK, BP, S, \
                            gram,       \
                            i, -1, j,   \
                            unary, u_unary, P)
    #print(i,s,j)
    #print(tag,u_tag)
    #print(tm1-tm0,time.time()-tm1)
    return (CYK,BP,S)

# Creates chart for sentence
def RunCYK(line, lex, gram):
    # Initialization
    CYK = []
    BP = []
    S = []
    words = line.split(' ')
    for i in range(len(words)+1):
        CYK.append([])
        BP.append([])
        S.append([])
        for j in range(len(words)+1):
            CYK[i].append({})
            BP[i].append({})
            S[i].append({})
    for i in range(1, len(words)+1):
        if words[i-1] in lex:
            for tag in lex[words[i-1]]:
                CYK[i-1][i][tag] = lex[words[i-1]][tag]
        else:
            CYK[i-1][i]['NN'] = 0

    # Recursion, assuming CNF (with unary productions)
    for j in range(1, len(words)+1):
        for i in range(j-2,-1,-1):
            for s in range(i+1, j):
                if len(CYK[s][j]) > 0:
                    for tag in itertools.product( \
                                   CYK[i][s], CYK[s][j]):
                        u_tag = (Unmask(tag[0], True), \
                                 Unmask(tag[1], False))
                        if not tag in gram[1] and \
                           not u_tag in gram[1]:
                            continue
                        P = CYK[i][s][tag[0]] + \
                                        CYK[s][j][tag[1]]
                        (CYK,BP,S) = AddToCYK(CYK, BP, S,\
                                        gram,      \
                                        i, s, j,   \
                                        tag, u_tag, P)
    return (CYK,BP,S)

# Returns probability for line being sentence
def CYKLineLogProb(line, lex, gram):
    CYK_result = RunCYK(line, lex, gram)
    if 'S' in CYK_result[0][0][len(line)]:
        logP = CYK_result[0][0][len(line)]['S']
        P = math.exp(logP)
    else:
        P = 0
    return P

# Checks if line can be valid sentence
def CYKCanLineExist(line, lex, gram):
    P = CYKLineProb(line, lex, gram)
    return P > 0

# Creates a highest probability tree for line
def CYKGetLineTree(line, lex, gram):
    t = Tree()
    CYK_result = RunCYK(line, lex, gram)
    t.ParseFromCYK(line, CYK_result)
    
    return t

# Removes all but maximum grammar derivations
def SparsifyGrammar(gram, d):
    res = ({},{})

    if d < 1:
        return gram

    for g in range(2):
        for tag in gram[g]:
            for val in gram[g][tag]:
                if not tag in res[g]:
                    res[g][tag] = {}
                    res[g][tag][val] = gram[g][tag][val]
                    P = gram[g][tag][val]
                elif gram[g][tag][val] > P:
                    res[g][tag] = {}
                    res[g][tag][val] = gram[g][tag][val]
                    P = gram[g][tag][val]
                elif gram[g][tag][val] == P:
                    res[g][tag][val] = gram[g][tag][val]
    
    return res 

# Creates string-forest for list of sentences
def ApplyCYK(lines, lex, gram):
    res = []
    i = 1
    timelog.timelog()
    tm = time.time()
    gram = SparsifyGrammar(gram, 1)
    for line in lines:
        if line.find('(') > -1:
            t = Tree()
            try:
                t.ParseFromString(line)
                line = t.LeavesToString()
            except Exception:
                pass
        print(line)
        print("Line length: ", len(line.split(' ')))
        res_tree = CYKGetLineTree(line, lex, gram)
        print("CNF:")
        print(res_tree.ToString())
        res_tree = RemoveCNF(res_tree)
        res_line = res_tree.ToString()
        print("Not CNF:")
        print(res_line)
        if res_line.strip(' ') == '()':
            t = Tree()
            t.head.data.label = 'S'
            for word in line.rstrip('\n').split(' '):
                tag_w = Tree.Node()
                tag_w.data.label = 'NN ' + word
                t.head.AddChild(tag_w)
            res_line = t.ToString()
        res.append(res_line)
        print("Applied CYK to " + str(i) + " lines.")
        print("Time: " + str(timelog.timelog()))
        i = i + 1
    print("Process time: " + str(time.time()-tm))
    
    return res
