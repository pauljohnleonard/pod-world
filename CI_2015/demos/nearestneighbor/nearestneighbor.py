# Perform nearest neighbour classification using training and test data from the
# MNINST digit data base.

import gzip
import cPickle
import numpy
import time

def calc_dist(a, b):
    """
     a and b are 1D arrays of the same size
     return dot product of the difference (square of the euclidean distance)
    """
    c = a - b
    return (c * c).sum()

def load_data(zipfile):
    """
    Load training and test data form the given zipfile
    returns training and test input and classifications
    """
    f = gzip.open(zipfile)
        
    # load data into the 3 data sets
    print " LOADING .....  DATA . . . . . ",
    training_set, validation_set, test_set = cPickle.load(f)    
    print " DONE"
        
    nTrain = len(training_set[0])    # use first nTrain training examples
    nTest = len(test_set[0])     # test first nTest test cases 
    
    print "    Training set size: ", nTrain
    print "        Test set size: ", nTest
        
    #training_input=training_set[0]
    # using numpy arrays will speed things up by a few orders of magnitude
    training_input = numpy.array(training_set[0])
        
    #test_input=test_set[0]
    test_input = numpy.array(test_set[0])
        
    test_output = test_set[1]
    training_output = training_set[1] 
    return training_input,training_output,test_input,test_output    


# compressed data 
filename = "./mnist/mnist_lite.pkl.gz"

training_input,training_output,test_input,test_output=load_data(filename)    
nTrain = len(training_input)    # use first nTrain training examples
nTest = len(test_input)         # test first nTest test cases 

# lets time this!! 
start = time.time()
        
        
#  
#  training_input      array of input vectors
#  training_output     array of classification 
#  test_input          array of input vectors
#  test_output         array of classification 
  
    
BIG = 1e32        #  just a very big distance
countCorrect = 0  #  counter for number of correct classifications
countFail = 0     #  counter for the incorrect classifications
    
for i in range(nTest):    # for all test cases
        
        #  mindist and jNearest  keep track of best distance so far
        mindist = BIG
        jNearest = -1
    
        for j in range(nTrain):
            dist = calc_dist(training_input[j], test_input[i])
            if dist < mindist:
                mindist = dist
                jNearest = j
     
        # Now see if we got it right ?
        if  training_output[jNearest] == test_output[i]:
            countCorrect += 1
        else:
            countFail += 1
         #   print i,":  " , (countCorrect*100.0)/(countCorrect+countFail), "%"
            
end = time.time()
    
print countCorrect, " out of ", nTest, " In ", end - start, " secs    ", (countCorrect * 100.0) / nTest, "%"




