# Get command line arguments and allow for IDLE manual
# argument input.
import sys
from trainers import *
from tree import *

def main(argv):
	if len(argv) != 3:
		print("Usage: <train filename> <smoothing (Y/N)>")
		return

	filename = sys.argv[1]
	smoothing = sys.argv[2]

	# Read input file
	file = open(filename, 'r')
	lines = file.readlines()
	file.close()

	# Create parameter file
	filename = filename.split('.')[0]
	filename = filename + '-' + smoothing

	if smoothing == 'y' or smoothing == 'Y':
		smoothing = True
	else:
		smoothing = False

	Train(filename, lines, smoothing)

	t = Tree()
	t.ParseFromString(lines[0])
	print(t)
	print(t.ToString())
	print(t.LeavesToString())
	print(t.CountLeaves())
	print(t.GramCount())


if __name__ == '__main__':
	main(sys.argv)