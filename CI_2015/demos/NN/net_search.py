# Program that searches for the weights to implement a boolean function.

import neuralnet
import math
import copy
import random

# define the size of the NN
n_in=2
n_hid=6
n_out=1


# define range and quantization of the guesses

min_weight=-2.0
max_weight=2.0
quant_weight=0.1
hh=quant_weight/2.0




def test_net(nn,training_in,training_out):
    """
     test the net and return an error estimate
    """
    error=0.0
    for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
        out=nn.fire(x)
        error += math.fabs(target[0]-out[0])
        
    return error


def random_weight():
    """
    returns a single random weight
    """ 
    w=min_weight-hh + (max_weight-min_weight+quant_weight)*random.random()
    www=round(w/quant_weight)*quant_weight
    return www

def random_weights():
    """
    Create a random set of weights for a network
    """
    
    w=[]
    w.append([])
    for i in range(n_hid):
        w[0].append([])
        for _ in range(n_in+1):
            w[0][i].append(random_weight())
            
    w.append([])
    for i in range(n_out):
        w[1].append([])
        for _ in range(n_hid+1):
            w[1][i].append(random_weight())
            
    return w


def mutate(weights_orig,mutate_amount):
    """
    Mutates the weights by a random amount.
    Not used in the example but you might find this useful.
    """
    
    # copy original into a new array
    w=copy.deepcopy(weights_orig)

    for layer in xrange(len(w)):
        for neuron in xrange(len(w[layer])):
            for i in xrange(len(w[layer][neuron])):
                w[layer][neuron][i] += random_weight()*mutate_amount 
     
    return w


# create a NeuralNet that we will try to optimize for the following training data
nn=neuralnet.Network2Layer(n_in,n_hid,n_out)

# XOR training data

training_in=[[0.0,0.0],[0.0,1.0],[1.0,0.0],[1.0,1.0]]
# training_out=[[0.0],[1.0],[1.0],[0.0]]
training_out=[[1.0],[1.0],[1.0],[0.]]


MAX_ITERS = 100000
TOL=0.0



def search():
    guess=random_weights()
    #print guess
    global best_guess
    best_error=1e32
    iter=0
    
    print "Iteration  error"
    
    while iter < MAX_ITERS:
        nn.set_weights(guess)
        error=test_net(nn,training_in,training_out)
        
        if error < best_error:
            best_guess=copy.deepcopy(guess)    # now copy so we don't mess up the best_guess
            best_error=error
            print iter,error
       
        if error <= TOL:
            break
             
        guess=random_weights()
        iter += 1
    
    
    success=best_error <= TOL
    

    if success:
        return iter
    else:
        print " Failed", " best error=",best_error
        return -1;
    
   
sum=0.0
N=100
for i in range(N):    
    it=search()
    if it == -1 :
        print "FAILED"
    else:
        sum += it
        
print "Average = ", sum/N 