# TODO   share code with net_search.

import net_sig as net
import math
import copy
import random

n_in=2
n_hid=2
n_out=1


# test the net and return an error estimate
def test_net_print(nn,training_in,training_out):
    error=0.0
    for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
        out=nn.fire(x)
        print x,"|",target,"|",out
        
    return error

# test the net and return an error estimate
def test_net(nn,training_in,training_out):
    error=0.0
    for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
        out=nn.fire(x)
        error += math.fabs(target[0]-out[0])
        
    return error

def random_weight():
    return (0.5-random.random())*factor

def random_weights():
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
    # copy original into a new array
    w=copy.deepcopy(weights_orig)

    for layer in xrange(len(w)):
        for neuron in xrange(len(w[layer])):
            for i in xrange(len(w[layer][neuron])):
                w[layer][neuron][i] += random_weight()*mutate_amount 
     
    return w


def set_weights(w,nn):
    for lay in xrange(len(w)):
        for neur in xrange(len(w[lay])):
            nn.set_weights(lay,neur,w[lay][neur])
            
# create a NeuralNet that we will try to optimize for the following training data

# XOR training data

training_in=[[0.,0.],[0.,1.],[1.,0.],[1.,1.]]
training_out=[[0.],[1.],[1.],[0.]]


MAX_ITERS = 100000

# A tolerance of 0.5 should ensure the netwrok works 
# if we interpret the output <0.5 as FASLE and >0.5 as TRUE  

TOL=0.5
best_error=1e32
factor=100.0
mutate_amount=1.0
iter=0
n_dim=12
MAX_TRY=n_dim*3


nn=net.Network2Layer(n_in,n_hid,n_out)

guess=random_weights()

#n_cnt=0

while iter < MAX_ITERS:
    set_weights(guess,nn)
    error=test_net(nn,training_in,training_out)
    
    if error < best_error:
        best_guess=copy.deepcopy(guess)    # now copy so we don't mess up the best_guess
        best_error=error
        print iter,error
   
        
    if error <= TOL:
        break
         
    guess=random_weights()   
    #guess=mutate(best_guess,mutate_amount)
    iter += 1


success=best_error <= TOL

if success:
    print " Success ", " Iters ",iter,"\n"
else:
    print " Failed", " best error=",best_error

nn.debug()

test_net_print(nn,training_in,training_out)
