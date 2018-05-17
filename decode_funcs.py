# Translates lines from lexical param file to logical data
def LexicalDecode(lex_lines):
    lex = {}
    for line in lex_lines:
        parts = line.rstrip('\n').split('\t')
        word = parts[0]
        for i in range(0, len(parts), 2):
            if i==0:
                continue
            tag = parts[i-1]
            if not word in lex:
                lex[word] = {}
            lex[word][tag] = parts[i]

    return lex

# Translates lines from grammatical param file to logical
# data
def GrammaticalDecode(gram_lines):
    gram_top_down = {}
    gram_bottom_up = {}
    for line in gram_lines:
        parts = line.rstrip('\n').split('\t')
        head = parts[1]
        tail = []
        for part in range(2, len(parts)):
            tail.append(part)
        tail = tuple(tail)
        if not head in gram_top_down:
            gram_top_down[head] = {}
        gram_top_down[head][tail] = float(parts[0])
        if not tail in gram_bottom_up:
            gram_bottom_up[tail] = {}
        gram_bottom_up[tail][head] = float(parts[0]) 

    return (gram_top_down, gram_bottom_up)
