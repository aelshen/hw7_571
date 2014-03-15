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
        
        sentence_pair.append( nltk.wordpunct_tokenize(sentence) )
        
        if len(sentence_pair) == 2:
            HobbsAlgorithm(sentence_pair, parser, result_file)
            sentence_pair = []
    
    data_file.close()
    result_file.close()
#==============================================================================    
#---------------------------------Functions------------------------------------
#==============================================================================
##-------------------------------------------------------------------------
## HobbsAlgorithm()
##-------------------------------------------------------------------------
##    Description:      Performs Hobb's algorithm on a set of sentences,
##                      finding acceptable antecedents for any pronouns found 
##                      in the second sentence of every pair passed in.
##
##    Arguments:        sentence_pair; a pair of lists, where each item is
##                          a list of tokens for a sentence
##                      parser; an NLTK build parser
##                      result_file; the file to output Hobb's results
##
##    Called by:        main()
##-------------------------------------------------------------------------
def HobbsAlgorithm(sentence_pair, parser, result_file):
    sentence_1 = parser.nbest_parse(sentence_pair[0], 1)
    sentence_2 = parser.nbest_parse(sentence_pair[1], 1)
    
    #if a valid parses found, apply algorithm
    if sentence_1 and sentence_2:
        sentence_1 = nltk.tree.ParentedTree.convert(sentence_1[0])
        sentence_2 = nltk.tree.ParentedTree.convert(sentence_2[0])
        
        
        candidate_antecedents = []
        case = None
        
        #Extract possible antecedents from the first sentence of the pair
        for x in sentence_1.subtrees():
            temp = x.node.__repr__()[:2]
            
            if temp == 'S[':
                candidate_antecedents.append((x,case))
            elif temp == 'NP':
                parent = x.parent().node.__repr__()[:2] 
                
                #if the parent of this NP is a VP,
                #then it is likely the object of a verb (ACC case)
                if parent == 'VP':
                    case= 'ACC'
               
                candidate_antecedents.append((x,case))
        
        
        pro = []
        case = None
        
        #Extract any pronouns from the second sentence
        for x in sentence_2.subtrees():
            temp = x.node.__repr__()[:3]
            
            #add to list of candidate antecedents if node is S or NP
            if temp[:2] == 'S[':
                candidate_antecedents.append((x,case))
            elif temp[:2] == 'NP':
                parent = x.parent().node.__repr__()[:2]
                if parent == 'VP':
                    case= 'ACC'
               
                candidate_antecedents.append((x,case))

            elif temp == ('PRP' or 'Pos'):
                #if current node is a pronoun (personal pronoun, possessive pronoun)
                #append to list of pronouns a tuple of
                #(str:pronoun,FeatStruct:pronoun feature structure, case:ACC or not, candidate_antecedents:list of all possible NP/S nodes that coudl be antecedent)
                pro.append((str(x.leaves()),x.node,case,candidate_antecedents[:]))
        
        result_file.write(sentence_1.flatten().pprint(margin=500) + os.linesep)
        result_file.write(sentence_2.flatten().pprint(margin=500) + os.linesep)
        
        s1 = sentence_1.pprint(margin=500)
        s2 = sentence_2.pprint(margin=500)
        
        for ref in pro:
            result_file.write(ref[0] + "\t" + s1 + " " + s2 + os.linesep)
            #for climbing the parse tree of sentence 1 from bottom-up
            for ante in reversed(ref[3]):
                #makes sure we aren't checking a pronoun against itself
                if ref[0] == str(ante[0].leaves()):
                    continue
                
                result_file.write(ante[0].pprint(margin=500) + os.linesep)
                result_file.write(' '.join(ante[0].leaves()) + os.linesep)
                
                try:
                    #try-block is necessary because S nodes (in my grammar)
                    #have no AGR values
                    fs_ante = ante[0].node["AGR"]
                    fs_pro = ref[1]["AGR"]
                    
                    #check for AGR agreement between pronoun and antecedent
                    agreement = fs_pro.unify(fs_ante)
                except:
                    agreement = False
                    pass
                
                case_ante = ante[1]
                case_pro = ref[2]
                
                if agreement:
                    if case_ante == case_pro:
                        result_file.write("Acceptable - preferred" + os.linesep)
                    else:
                        result_file.write("Acceptable" + os.linesep)
                else:
                    result_file.write("Reject" + os.linesep)
                    
                result_file.write(os.linesep)
                
        result_file.write(os.linesep)
    else:
        print("Parse error: there wasn't a valid parse for both sentences")

#==============================================================================    
#------------------------------------------------------------------------------
#==============================================================================
if __name__ == "__main__":
    sys.exit( main() )