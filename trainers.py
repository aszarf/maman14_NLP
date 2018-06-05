# Main training module

from tree import *
import math
import random
import CNF

LEX_TEMPLATE = "%s\t%s\t%f"
RULE_TEMPLATE = "%f\t%s\t%s"
RULE_TEMPLATE_CNF = "%s\t%s\t%s %s"

def calc_count(lines):
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
    
    return gram_count, leaves_count

def Train(filepath, lines, smoothing):
    gram_count, leaves_count = calc_count(lines)
    
    leaves_sum = float(reduce(lambda x,y: x+y, leaves_count.values()))
    lines_lex = []
    for key in leaves_count:
        exists_line = filter(lambda x: x.startswith(key[1] + '\t'), lines_lex)
        logprob = -math.log(leaves_count[key]/leaves_sum)
        if len(exists_line) == 0:
            line = LEX_TEMPLATE % (key[1], key[0], logprob)
        else:
            line = exists_line[0]
            line = line + "\t%s\t%f" % (key[0], logprob)
        lines_lex.append(line)
    open(filepath + ".lex", "wb").write('\n'.join(lines_lex))
    
    gram_sum = float(reduce(lambda x,y: x+y, gram_count.values()))
    lines_gram = []
    for key in gram_count:
        logprob = -math.log(gram_count[key]/gram_sum)
        line = RULE_TEMPLATE % (logprob, key[0], ' '.join(key[1]))
        lines_gram.append(line)
    open(filepath + ".gram", "wb").write('\n'.join(lines_gram))
        
    print "Train is done"
        
    return True
	
def create_new_symbol(root, childs, index):
    res = root
    for i,j in enumerate(childs):
        if i == index:
            res = res + '*' + childs[i]
        else:
            res = res + '-' + childs[i]
    return res
    
def convert_to_CNF(filepath, lines, h):    
    lines_for_count = []
    for i,line in enumerate(lines):
        print i
        t = Tree()
        t.ParseFromString(line)
        t2 = CNF.ApplyCNF(t,h)
        lines_for_count.append(t2.ToString())

        gram_count, leaves_count = calc_count(lines_for_count)

    gram_sum = float(reduce(lambda x,y: x+y, gram_count.values()))
    lines_gram = []
    for key in gram_count:
        logprob = -math.log(gram_count[key]/gram_sum)
        line = RULE_TEMPLATE % (logprob, key[0], ' '.join(key[1]))
        lines_gram.append(line)
    open(filepath + ".gram.CNF", "wb").write('\n'.join(lines_gram))
    print "CNF is done"
    return True
