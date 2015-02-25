"""
Demonstrates a incremental search for finding the weights of a neural net.

Set the random_search = True for a random search
    random_search=False will use incremental improvement using a mutation determined by amount
                     
"""


import brain
import math
import copy
import random

random_search=False


# initial weights will be in  the range (-0.5 to 0.5)   * scale
# does changing this effect the performance ?
scale=100.0

# amount of mutation for the incremental improvement search
# each weight is mutated by a factor in the range (-0.5 to 0.5)   * scale * mutate_amount
mutate_amount=2.0


# neural net size parameters.
n_in=2
n_hid=2
n_out=1


# define some useful functions.


# display the performance of the network
def test_net_print(nn,training_in,training_out):
    """
    nn          is a neural net.
    training_in is a list of inputs
    training_out is a parallel list of the training outputs.
    
    print a list of inputs, target outputs and actual outputs
    """
    for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
        out=nn.ffwd(x)
        print x,"|",target,"|",out
        
    
# test the net and return an error estimate using training data
def test_net(nn,training_in,training_out):
    error=0.0
    for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
        out=nn.ffwd(x)
        error += math.fabs(target[0]-out[0])
        
    return error

def random_weight(scale):
    """
    generate a single random weight in the rage (-0.5 to 0.5)   * scale
    """
    return (0.5-random.random())*scale

def random_weights(scale):
    """
    Create a whole network of weights  (using the sizes defined by n_in n_hid and n_out)
    Note that bias weights are also created at the end of the list of weights.
    Each weight is in the rage (-0.5 to 0.5)   * scale 
    """
    w=[]
    w.append([])
    for i in range(n_hid):
        w[0].append([])
        for _ in range(n_in+1):
            w[0][i].append(random_weight(scale))
            
    w.append([])
    for i in range(n_out):
        w[1].append([])
        for _ in range(n_hid+1):
            w[1][i].append(random_weight(scale))
            
    return w


# example showing how you might mutate the weights
def mutate(weights_orig,mutate_amount):
    # copy original into a new array
    w=copy.deepcopy(weights_orig)

    for layer in xrange(len(w)):
        for neuron in xrange(len(w[layer])):
            for i in xrange(len(w[layer][neuron])):
                w[layer][neuron][i] += random_weight(mutate_amount) 
     
    return w


            
# create a NeuralNet that we will try to optimise for the following training data

# XOR training data

training_in=[[0.,0.],[0.,1.],[1.,0.],[1.,1.]]
training_out=[[0.],[1.],[1.],[0.]]


MAX_ITERS = 100000

# A tolerance of 0.5 should ensure the netwrok works 
# if we interpret the output <0.5 as FASLE and >0.5 as TRUE  

TOL=0.5

best_error=1e32

iter=0


# initial random guess
guess=random_weights(scale)

# create a brain using guess for the initial  weights 
nn=brain.FeedForwardBrain(weight=guess)

# debug 
print nn.weight


# start the search loop
while iter < MAX_ITERS:
    
    # set the weights using the the current guess
    nn.setWeights(guess)
    
    # test the network and measure the error
    error=test_net(nn,training_in,training_out)
    
    # if the error is better previous best then update best_guess
    if error < best_error:
        best_guess=copy.deepcopy(guess)    # now copy so we don't mess up the best_guess
        best_error=error
        print iter,error
   
    
    # Have we satisfied the stopping criteria yet? 
    if error <= TOL:
        break

   
    guess=mutate(best_guess,mutate_amount*scale)    # make a guess by mutating the best guess so far
        
    iter += 1


success=best_error <= TOL

if success:
    print " Success ", " Iters ",iter,"\n"
    brain.saveBrain(nn)    # save brain for later use
else:
    print " Failed", " best error=",best_error

print nn.weight

test_net_print(nn,training_in,training_out)
