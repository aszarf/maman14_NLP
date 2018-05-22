# CYK Functions
from tree import *
import math

# Creates chart for sentence
def RunCYK(line, lex, gram):
    # Initialization
    CYK = []
    BP = []
    S = []
    for i in range(len(words)):
        CYK.append([])
        BP.append([])
        S.append([])
        for j in range(len(words)+1):
            CYK[i].append({})
            BP[i].append({})
            S[i].append({})
    words = line.split(' ')
    for i in range(len(words)):
        if words[i] in lex:
            for tag in lex[words[i]]:
                CYK[i][i+1][tag] = lex[words[i]][tag]

    # Recursion, assuming CNF
    for length in range(1, len(words)-1):
        for i in range(len(words) - length):
            j = i + length
            for s in range(i+1, j-1):
                for Y in CYK[i][s]:
                    for Z in CYK[s+1][j]:
                        if (Y,Z) in gram[1]:
                            for X in gram[1][(Y,Z)]:
                                P1 = gram[1][(Y,Z)][X]
                                P2 = CYK[i][s][Y]
                                P3 = CYK[s+1][j][Z]
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

# Creates forest for list of sentences
def ApplyCYK(lines, lex, gram):
    res = []

    for line in lines:
        t = Tree()
        if line.find('(') > -1:
            try:
                t.ParseFromString(line)
                line = t.LeavesToString()
            except Exception:
                pass
        res.append(CYKGetLineTree(line, lex, gram))

    return res
