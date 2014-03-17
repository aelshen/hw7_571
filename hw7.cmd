#######################################################
##
## hw7 Condor command file
## Ahmad Elshenawy
## Ling 571
## Mar 18, 2014
##
#######################################################

executable      = hobbs.sh
getenv		= true
error		= hw7.err
log		= hw7.log
arguments 	= "grammar.fcfg coref_sentences.txt results-unannotated"
transfer_executable = false
Queue
