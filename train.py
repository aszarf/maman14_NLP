# Get command line arguments and allow for IDLE manual
# argument input.
import sys

if sys.modules['idlelib']:
    print("Usage: <train filename> <smoothing (Y/N)>")
    sys.argv.extend(input("Args: ").split())

filename = sys.argv[1]
smoothing = sys.argv[2]

# Read input file
file = open(filename, 'r')
lines = file.readlines()
file.close()

# Create parameter file
from trainers import *

filename = filename.split('.')[0]
filename = filename + '-' + smoothing

if smoothing == 'y' or smoothing == 'Y':
    smoothing = True
else:
    smoothing = False

Train(filename, lines, smoothing)

from tree import *

t = Tree()
t.ParseFromString(lines[0])
print(t)
print(t.ToString())
print(t.LeavesToString())
print(t.CountLeaves())
print(t.GramCount())
