"""  
 
 Perceptron training example

 This is example has 3 binary inputs and a single output.

""" 

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
    
    # assume last connection is the bias  
    sum=wVec[n-1]  
    
    for i in range(n-1):
        sum += xVec[i]*wVec[i]
        
    if sum > 0.0:
        return 1.0
    else:
        return 0.0    


# training data is a list of inputs and target values.
 
training_in = [ [0.,0.,0.], \
                [0.,0.,1.], \
                [0.,1.,0.], \
                [0.,1.,1.], \
                [1.,0.,0.], \
                [1.,0.,1.], \
                [1.,1.,0.], \
                [1.,1.,1.]]    

training_out = [ 0.,0.,0.,1.,1.,1.,1.,1.] 

#Deduce the number of inputs from the first training data

n=len(training_in[0])    # set n to the number of inputs
   
assert len(training_in) == len(training_out)

w=[0.,0.,0.,0.]    # initial weights

converged=False    # flag for convergence
beta=6.0           # learning rate
iter=1             # iteration counter
tolerance=1e-6     # convergence criterea
max_iters=100      # maximum number of iterations before we give up.

while iter < max_iters and not converged:
    print "** iter = ",iter
    print "      x        t y           w "
    iter += 1
    converged=True
    for x,t in zip(training_in,training_out):  #   iterate on the list of input target pairs
        y=fire(x,w)
        print x,int(t),int(y),w    # display what is happening
        if abs(t-y) > tolerance:
            converged=False
            
          
        #  use the perceptron training rule to update the weights  
        for i in range(n):
            w[i]=w[i]+beta*(t-y)*x[i]
            
        # basis weight is connected to a constant 1    
        w[n]=w[n]+beta*(t-y)
            
            
        

        
           
        
