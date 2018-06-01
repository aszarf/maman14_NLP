# Main training module

from tree import *
import math
import random
# import CNF

LEX_TEMPLATE = "%s\t%s\t%f"
RULE_TEMPLATE = "%f\t%s\t%s"
RULE_TEMPLATE_CNF = "%s\t%s\t%s %s"

def Train(filepath, lines, smoothing):
    
    # for line in lines:
        # t = Tree()
        # t.ParseFromString(line)
        # CNF.ApplyCNF(t,0)
    # return
    
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
    
# def gen_unused_symbol(symbol, symbols):
    # while symbol in symbols:
        # rand_chr = chr(random.randint(ord('A'), ord('Z')))
        # symbol = symbol + rand_chr
    # return symbol
	
def create_new_symbol(root, childs, index):
    res = root
    for i,j in enumerate(childs):
        if i == index:
            res = res + '*' + childs[i]
        else:
            res = res + '-' + childs[i]
    return res
    
def convert_to_CNF(filepath, lines):
    ret_lines = []
    # new_symbols = []
    for line in lines:
        line = line[:-1] # without \n
        logprob, root, childs = line.split('\t')
        childs = childs.split(' ')
        if len(childs) > 2:
            new_lines = []
            # new_symbol_right = gen_unused_symbol(root+'0', new_symbols)
            root_new_symbol = create_new_symbol(root, childs, 0)
            new_symbol_right = create_new_symbol(root, childs, 1)
            # new_symbols.append(new_symbol_right)
                
            rule = RULE_TEMPLATE_CNF % (logprob, root_new_symbol, childs[0], new_symbol_right)
            new_lines.append(rule)
            for i in xrange(1, len(childs)-2):
                new_symbol_left = new_symbol_right
                # new_symbol_right = gen_unused_symbol(root+str(i), new_symbols)
                new_symbol_right = create_new_symbol(root, childs, i+1)
                # new_symbols.append(new_symbol_right)
                rule = RULE_TEMPLATE_CNF % (logprob, new_symbol_left, childs[i], new_symbol_right)
                new_lines.append(rule)
            rule = RULE_TEMPLATE_CNF % (logprob, new_symbol_right, childs[-2], childs[-1])
            new_lines.append(rule)
            
            ret_lines = ret_lines + new_lines
        else:
            ret_lines.append(line)
        
    open(filepath + '.CNF', 'wb').write('\n'.join(ret_lines))
    print "CNF is done"
    return True
    
