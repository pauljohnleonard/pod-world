import gzip
import cPickle
import numpy

def read(filename):
      # compressed data 
    #data="mnist_lite.pkl.gz"
    f=gzip.open(filename)
    
    # load data into the 3 data sets
    print " LOADING .....  DATA . . . . . ",
    training_set,validation_set,test_set=cPickle.load(f)    
    print " DONE"
      
    nTrain=len(training_set[0])    # use first nTrain training examples
    nTest=len(test_set[0])     # test first nTest test cases 
    print "    Training set size: ",nTrain
    print "        Test set size: ",nTest
    
     
    
    training_input=numpy.array(training_set[0])
    test_input=numpy.array(test_set[0])    
    test_output=test_set[1]
    training_output=training_set[1] 
    
    return training_input,training_output,test_input,test_output
    