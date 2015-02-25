"""

DEMO showing a 2 layer network learning XOR using backprop.

Note that this does not always converge!  

"""

import backprop
import math


n_in=2
n_hid=2
n_out=1

# test the net and return an error estimate
def test_net(nn,training_in,training_out):
    error=0.0
    for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
        out=nn.ffwd(x)
        for t,o in zip(target,out):
            error += math.fabs(t-o)
        
    return error



# test the net and return an error estimate
def train_net(nn,training_in,training_out):
    for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
        nn.bpgt(x,target)  
  

# test the net and return an error estimate
def test_net_print(nn,training_in,training_out):
    error=0.0
    for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
        out=nn.ffwd(x)
        print x,"|",target,"|",out
        
    return error


def doit():
    # create a NeuralNet 
    nn=backprop.BackPropBrain([n_in,n_hid,n_out])
    
    
    # XOR training data
    
    training_in=[[0,0],[0,1],[1,0],[1,1]]
    training_out=[[0],[1],[1],[0]]
    
    
    MAX_ITERS = 100000
    
    #print guess
    
    TOL=0.1
    best_error=1e32
    iter=0
    
    while iter < MAX_ITERS:
    
        # Train with one pass through the training data
        train_net(nn,training_in,training_out)
        
        # Check the error.
        error=test_net(nn,training_in,training_out)
        
        if error < best_error:
            best_error=error
            print iter,error
       
        if error <= TOL:
            break
             
        iter += 1
    
    
    success=best_error <= TOL
    
    if success:
        print " Success ", " Iters ",iter,"\n"
    
    else:
        print " Failed", " best error=",best_error
    
    
    test_net_print(nn,training_in,training_out)
    
    
if __name__ == "__main__":
    doit()
