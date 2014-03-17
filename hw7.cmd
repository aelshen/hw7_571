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
output		= results
error		= hw7.err
log		= hw7.log
arguments 	= "grammar.fcfg coref_sentences.txt results"
transfer_executable = false
Queue
