# Main decoding module

from CYK import *
from tree import *
from decode_funcs import *

def Decode(filename, lines, lex_lines, gram_lines):

    # Create list of lex probs
    lex = LexicalDecode(lex_lines)

    # Create lists of gram probs
    gram = GrammaticalDecode(gram_lines)

    # Use CYK to create relevant tree string for each line
    forest = ApplyCYK(lines, lex, gram)

    # Output forest to file
    output = open(filename + '.parsed', 'w')
    output_lines = []

    for t in forest:
        line = t + '\n'
        output_lines.append(line)

    output.writelines(output_lines)    
    output.close()    
    
    return
