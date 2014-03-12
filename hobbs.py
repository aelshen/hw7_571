'''
#==============================================================================
hobbs.py
Created on Mar 17, 2014
@author: aelshen
#==============================================================================
'''
from __future__ import print_function
import os
import sys
import nltk
#==============================================================================
#--------------------------------Constants-------------------------------------
#==============================================================================
DEBUG = True
PRONOUNS = ['their', 'Their', 'this', 'them', 'They']
#==============================================================================
#-----------------------------------Main---------------------------------------
#==============================================================================
def main():
    if len(sys.argv) < 4:
        print("hobbs.py requires 3 arguments" 
               + os.linesep + "(1)grammar file"
               + os.linesep + "(2)test data file"
               + os.linesep + "(3)result file")
        sys.exit()
    
    grammar_file = "file:" + sys.argv[1]
    
    grammar = nltk.data.load(grammar_file)
    data_file = open(sys.argv[2], 'r')
    
    #open and close result file to empty it, 
    #then reopen with appending privileges
    result_file = open(sys.argv[3], 'w')
    result_file.close()
    result_file = open(sys.argv[3], 'a')
    
    #build parser
    parser = nltk.parse.FeatureEarleyChartParser(grammar)
    sentence_pair = []
    #read through all the lines in the data file
    for sentence in data_file.readlines():
        if not sentence.strip():
            continue
        
        if len(sentence_pair) < 2:
            sentence_pair.append( nltk.wordpunct_tokenize(sentence) )
        else:
            HobbsAlgorithm(sentence_pair, parser, result_file)
            sentence_pair = [nltk.wordpunct_tokenize(sentence)]

    
    
    data_file.close()
    result_file.close()
#==============================================================================    
#---------------------------------Functions------------------------------------
#==============================================================================
##-------------------------------------------------------------------------
## HobbsAlgorithm()
##-------------------------------------------------------------------------
##    Description:        description
##
##    Arguments:        arguments
##
##    Calls:                calls
##
##        Returns:            returns
##-------------------------------------------------------------------------
def HobbsAlgorithm(sentence_pair, parser, result_file):
    sentence_1 = parser.nbest_parse(sentence_pair[0], 1)
    sentence_2 = parser.nbest_parse(sentence_pair[1], 1)
    
    #if a valid parse was found, apply algorithm
    if sentence_1 and sentence_2:
        sentence_1 = nltk.tree.ParentedTree.convert(sentence_1[0])
        sentence_2 = nltk.tree.ParentedTree.convert(sentence_2[0])
        
        candidate_antecedents = []
        
        for x in sentence_1.subtrees():
            temp = x.node.__repr__()[:2]
            if temp == 'NP':
                parent = x.parent().node.__repr__()[:2] 
                
                #x.node returns the FeatStruct for this subtree
                if parent == 'VP':
                    candidate_antecedents.append((x,'ACC'))
                else:
                    candidate_antecedents.append((x,'NOM'))
        
        #find if the second sentence has any pronouns 
        pro = []
        for leaf in sentence_2.pos():
            if leaf[0] in PRONOUNS:
                pro.append(leaf)
        
        result_file.write(sentence_1.flatten().pprint(margin=500) + os.linesep)
        result_file.write(sentence_2.flatten().pprint(margin=500) + os.linesep)
        
        s1 = sentence_1.pprint(margin=500)
        s2 = sentence_2.pprint(margin=500)
        
        for ref in pro:
            result_file.write(ref[0] + "\t" + s1 + " " + s2 + os.linesep)
            for ante in reversed(candidate_antecedents):
                result_file.write(ante[0].pprint(margin=500) + os.linesep)
                result_file.write(' '.join(ante[0].leaves()) + os.linesep)
                
                fs_ante = ante[0].node["AGR"]
                fs_pro = ref[1]["AGR"]
                
                agreement = fs_pro.unify(fs_ante)
                
                if agreement:
                    result_file.write("Accept" + os.linesep)
                else:
                    result_file.write("Reject" + os.linesep)
                    
                result_file.write(os.linesep)
                
        result_file.write(os.linesep)
    else:
        print("Parse error: there wasn't a valid parse for both sentences")

#==============================================================================    
#----------------------------------Classes-------------------------------------
#==============================================================================
##-------------------------------------------------------------------------
## Class Classname
##-------------------------------------------------------------------------
##    Description:        desciription
##
##    Arguments:         arguments
##
##
##    Properties:         properties
##
##    Calls:                  calls
##
##-------------------------------------------------------------------------
class Classname:
    def __init__(self):
        self.x = 0

#==============================================================================    
#------------------------------------------------------------------------------
#==============================================================================
if __name__ == "__main__":
    sys.exit( main() )