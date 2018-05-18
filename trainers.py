# Main training module

from tree import *
import math

def Train(filename, lines, smoothing):
    
    leaves_count = {}
    gram_count = {}
    for line in lines:
        t = Tree()
        t.ParseFromString(line)
        leaves_dict = t.CountLeaves()
        gram_dict = t.GramCount()
        
        for key in leaves_dict.keys():
            if not key in leaves_count.keys():
                leaves_count[key] = leaves_dict[key]
            leaves_count[key] = leaves_count[key] + leaves_dict[key]
                
        for key in gram_dict.keys():
            if not key in gram_count.keys():
                gram_count[key] = gram_dict[key]
            gram_count[key] = gram_count[key] + gram_dict[key]
    
    leaves_sum = float(reduce(lambda x,y: x+y, leaves_count.values()))
    buf = ''
    for key in leaves_count:
        prob = -math.log(leaves_count[key]/leaves_sum)
        line = "%s\t%s\t%f\n" % (key[1], key[0], prob)
        buf = buf + line
    open(filename + ".lex", "wb").write(buf)
    
    gram_sum = float(reduce(lambda x,y: x+y, gram_count.values()))
    buf = ''
    for key in gram_count:
        prob = -math.log(gram_count[key]/gram_sum)
        line = "%f\t%s\t%s\n" % (prob, key[0], ' '.join(key[1]))
        buf = buf + line
    open(filename + ".gram", "wb").write(buf)
        
    return True
