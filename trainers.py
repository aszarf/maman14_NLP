# Main training module

from tree import *

def Train(filename, lines, smoothing):
    
    leaves_dict_forest = {}
    gram_dict_forest = {}
    for line in lines:
        t = Tree()
        t.ParseFromString(line)
        leaves_dict = t.CountLeaves()
        gram_dict = t.GramCount()
        
        for key in leaves_dict.keys():
            if key in leaves_dict_forest.keys():
                leaves_dict_forest[key] = leaves_dict_forest[key] + leaves_dict[key]
            else:
                leaves_dict_forest[key] = leaves_dict[key]
                
        for key in gram_dict.keys():
            if key in gram_dict_forest.keys():
                gram_dict_forest[key] = gram_dict_forest[key] + gram_dict[key]
            else:
                gram_dict_forest[key] = gram_dict[key]
    
    # TODO: write lex file 
    # TODO: write gram file
    
    
    # Translate lines into forest

    # Calculate lex probs

    # Write lex file
    
    # Calculate gram probs

    # Write gram file
    
    return
