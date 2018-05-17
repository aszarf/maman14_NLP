# Main training module

from tree import *

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
                leaves_count[key] = 0
            leaves_count[key] = leaves_count[key] + leaves_dict[key]
                
        for key in gram_dict.keys():
            if not key in gram_count.keys():
                gram_count[key] = 0
            gram_count[key] = gram_count[key] + gram_dict[key]

    # TODO: calculate logprobs
    # TODO: write lex file 
    # TODO: write gram file
    
    return
