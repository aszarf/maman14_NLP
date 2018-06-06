import sys
from decoders import *

def main(argv):
    # Get command line arguments and allow for IDLE manual
    # argument input.
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <test filename> <params...>")
            sys.argv.extend(input("Args: ").split())
        
    if len(argv) != 4:
        print("Usage: <test filename> <params...>")
        return

    filename = sys.argv[1]
    lex = sys.argv[2]
    gram = sys.argv[3]

    # Read input file
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()

    # Read lexical parameter file
    file = open(lex, 'r')
    lex_lines = file.readlines()
    file.close()

    # Read grammatical parameter file
    file = open(gram, 'r')
    gram_lines = file.readlines()
    file.close()

    # Create tag file

    filename = filename.split('.')[0]

    lex = lex.split('.')[0]
    lex = lex.split('-')
    if len(lex) > 2:
        lex = lex[2]
        filename = filename + '-' + lex

    Decode(filename, lines, lex_lines, gram_lines)

if __name__ == '__main__':
    main(sys.argv)
