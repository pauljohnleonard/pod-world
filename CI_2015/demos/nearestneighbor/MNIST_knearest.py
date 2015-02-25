# Does the classification of the test data for the MNINST digit data base.
# Using the k-nearest scheme.
# 

import gzip
import cPickle
import numpy
import time
import sys
import knearest


# name of the data set to test
data=   "./mnist/mnist.pkl.gz" # 
 
 
 
def load_data(zipfile):
    """
    Load training and test data form the given zipfile
    returns training and test input and classifications
    """
    f = gzip.open(zipfile)
        
    # load data into the 3 data sets
    print " LOADING ..... ",zipfile,
    training_set, validation_set, test_set = cPickle.load(f)    
    print " DONE"
        
    
    #training_input=training_set[0]
    # using numpy arrays will speed things up by a few orders of magnitude
    training_input = numpy.array(training_set[0])
        
    #test_input=test_set[0]
    test_input = numpy.array(test_set[0])
        
    test_output = test_set[1]
    training_output = training_set[1] 
    return training_input,training_output,test_input,test_output    

def calc_dist(a,b):
    """
    Calculate dot product of a and b
    Uses built in numpy to speed things up.
    """
    c=a-b
    return (c*c).sum()


def doit(k):    
        # compressed data 
   
    
    training_input,training_output,test_input,test_output=load_data(data)    
    
    # training_input is a list of input vectors
    # training_out  is a corresponding list of classifications
      
    nTest=len(test_input)           
    nTrain=len(training_input)     
     
    print "    Training set size: ",nTrain
    print "        Test set size: ",nTest
     
    BIG=1e32
        
    countCorrect = 0    #  counter for number of correct classifications
    countFail = 0       #  counter for incorrect
        
    for i in range(nTest):    # for all test cases
        
        kn = knearest.Knearest(k)   # helper to do the k nearest
       
        for j in range(nTrain):
            dist = calc_dist(training_input[j], test_input[i])
            kn.add(dist, training_output[j])
      
        # look at the result
        result = kn.get_knearest()
              
        if  result == test_output[i]:
            countCorrect += 1
        else:
            countFail += 1
      
            
    print " k=", k, "  ", countCorrect, "/", nTest, (countCorrect * 100.0) / nTest, "%"


if __name__ == "__main__":

    
# set k for the k nearest scheme
    for k in range(4):
        doit(k+1)
