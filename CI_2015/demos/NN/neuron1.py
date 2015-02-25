# This program will print out the truth table for a single neuron 

# The next line sets the weights of the neuron.
# Note that the last weight is for the bias OR threshold value.

weights=[1.0,-2.0,1.0,1.0]

def fire(xVec,wVec):
    """
        Implements a single threshold perceptron 
        
        xVec  is the input vector
        wVec  is the weight vector of the neuron connections
        
        The size of wVec is 1 greater than xVec
        The wVec[len(wVec)-1] represents the bais value
         
        returns 1 or 0
    """
    
    n=len(wVec)

#  Example showing how to implement a single neuron.


def fire(input,weights):
    
    # assume last connection is the bias  
    n=len(weights)
    sum=weights[n-1]  
    
    for i in range(n-1):
        sum += weights[i]*input[i]
        
    if sum > 0.0:
        return 1.0
    else:
        return 0.0    

## MAIN CODE STARTS HERE



# Now visit all the possible binary inputs and print out
# the output of the neuron
print "X1 X2 X3    OUTPUT"
for x1 in range(2):                 # range(2) means  x1 will take the values 0 and 1
    for x2 in range(2):
        for x3 in range(2):
            input=[x1,x2,x3]
            output=fire(input,weights)
            print "",x1,"",x2,"",x3,"   ",output
            
            

