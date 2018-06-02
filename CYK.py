# CYK Functions
from tree import *
from CNF import *
import math
import timelog

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

    # Recursion, assuming CNF
    for j in range(1, len(words)+1):
        for i in range(j-2,-1,-1):
            for s in range(i+1, j):
                for Y in CYK[i][s]:
                    P2 = CYK[i][s][Y]
                    for Z in CYK[s][j]:
                        P3 = CYK[s][j][Z]
                        if (Y,Z) in gram[1]:
                            for X in gram[1][(Y,Z)]:
                                P1 = gram[1][(Y,Z)][X]
                                P = P1+P2+P3
                                if X in CYK[i][j]:
                                    if P > CYK[i][j][X]:
                                        CYK[i][j][X] = P
                                        BP[i][j][X] = (Y,Z)
                                        S[i][j][X] = s
                                else:
                                    CYK[i][j][X] = P
                                    BP[i][j][X] = (Y,Z)
                                    S[i][j][X] = s
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
def SparsifyGrammar(gram):
    res = ({},{})

    P = 0
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
    for line in lines:
        if line.find('(') > -1:
            t = Tree()
            try:
                t.ParseFromString(line)
                line = t.LeavesToString()
            except Exception:
                pass
        gram = SparsifyGrammar(gram)
        res_tree = CYKGetLineTree(line, lex, gram)
        res_tree = RemoveCNF(res_tree)
        res_line = res_tree.ToString()
        if res_line.strip(' ') == '()':
            t = Tree()
            t.head.data.label = 'S'
            for word in line.rstrip('\n').split(' '):
                w = Tree.Node()
                w.data.label = word
                tag_w = Tree.Node()
                tag_w.data.label = 'NN'
                tag_w.AddChild(w)
                t.head.AddChild(tag_w)
            res_line = t.ToString()
        res.append(res_line)
        print("Applied CYK to " + str(i) + " lines.")
        i = i + 1
    print("Process time: " + str(timelog.timelog()))
    
    return res
