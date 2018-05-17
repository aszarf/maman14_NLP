# Main decoding module

from CYK import *
from tree import *
from decode_funcs import *

def Decode(filename, lines, lex_lines, gram_lines):

    # Create list of lex probs
    lex = LexicalDecode(lex_lines)

    # Create lists of gram probs
    gram = GrammaticalDecode(gram_lines)

    # Use CYK to create relevant tree for each line

    # Output forest to file
    
    return
