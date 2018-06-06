import sys
from trainers import *
from tree import *

def main(argv):
    # Get command line arguments and allow for IDLE manual
    # argument input.
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <train filepath> <smoothing (Y/N)>")
            sys.argv.extend(input("Args: ").split())

    if len(argv) != 3:
        print("Usage: <train filepath> <smoothing (Y/N)>")
        return

    filepath = sys.argv[1]
    smoothing = sys.argv[2]

    # Read input file
    file = open(filepath, 'r')
    lines = file.readlines()
    file.close()

    # Create parameter file
    filepath = filepath.split('.')[0]
    filepath = filepath + '-' + smoothing

    if smoothing == 'y' or smoothing == 'Y':
        smoothing = True
    else:
        smoothing = False

    Train(filepath, lines, smoothing)

    convert_to_CNF(filepath, lines, -1)
    convert_to_CNF(filepath, lines, 0)
    convert_to_CNF(filepath, lines, 1)
    
if __name__ == '__main__':
    main(sys.argv)
