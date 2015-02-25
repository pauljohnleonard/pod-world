"""
Perform nearest neighbour classification using training 
from the CI tutorial sheet
"""

def calc_dist(a, b):
    """
     a and b are 1D arrays of the same size
     return dot product of the difference (square of the Euclidean distance)
     Since we only this to compare distances there is no need to take the square root.
     So we are really returning the square of the eucledian distance.
    """
    sum=0
    for aa,bb in zip(a,b):    # This is how python iterates on 2 arrays at the same time.
        sum+= (aa-bb)*(aa-bb)
        
    return sum

def load_data():
    
    # load training data from tutorial sheet
    # Input is a list of 2D points
    training_input =[[1,1],[2,1],[2,2]]
    # Output class is one of many
    training_output=[1,2,3]
    
    return training_input,training_output # You can return a number of objects from a python function  


training_input,training_output=load_data()    
nTrain = len(training_input)    #  nTrain is number of training examples
        
#  
#  training_input      array of input vectors
#  training_output     array of classification 

  
    
BIG = 1e32        #  just a very big distance
countCorrect = 0  #  counter for number of correct classifications
countFail = 0     #  counter for the incorrect classifications
    
while(True):    # for all test cases
        
        #  mindist and jNearest  keep track of best distance so far
        mindist = BIG
        jNearest = -1
        
        
        #  prompt the user for a point  (2D)  as a string
        str=raw_input(" enter a point. e.g. 4.6 5.7 : ")
        xx=str.split()     # split string into substrings
        
        # create an array to hold the 2 values
        test_input=[]
        
        # convert the strings into floats
        for x in xx:
            test_input.append(float(x))
            
            
        print test_input
        
        # test_input should now have 2 values.
        # find the nearest point in the training data
        for j in range(nTrain):
            dist = calc_dist(training_input[j], test_input)
            if dist < mindist:
                mindist = dist
                jNearest = j
     
        # Now see if we got it right ?
        print "class of ",test_input[0],test_input[1]," is :",training_output[jNearest]   



