# CYK Functions

# Creates tree for sentence
def CYK(line, lex, gram):
    res = ''

    # TODO: Implement CYK
    
    return res

# Creates forest for list of sentences
def ApplyCYK(lines, lex, gram):
    res = []

    for line in lines:
        res.append(CYK(line, lex, gram))

    return res
