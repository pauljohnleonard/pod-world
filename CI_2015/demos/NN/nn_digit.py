# backpropagation example using the MNIST data set.
# This is very slow using python even with numpy  (see Dr leonards JAVA version !!!!)

import backprop_nmpy as backprop
import math
import readdata




training_in,training_output_class,test_in,test_output_class=readdata.read("../mnist/mnist_lite.pkl.gz")
  
  

n_in=len(training_in[0])                 # size of each inputs (input neurons) 
n_hid=n_in
n_out=10

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
    print "training:..",
    for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
        nn.bpgt(x,target)
        #print ".",
        #break
    print
  

# test the net and return an error estimate
def test_net_print(nn,training_in,training_out):
    print "testing ...",
    error=0.0
    for x,target in zip(training_in,training_out):     # clever way to iterate on 2 parallel lists!!
        out=nn.ffwd(x)
        print x,"|",target,"|",out
    
    
    print
    return error


def doit():
    # create a NeuralNet 
    nn=backprop.BackPropBrain([n_in,n_out])
    
    
    
    # for a nureal net we want an binary output vector
    # class to vec maps the integer class onto a binary vector with the appropriate  entry set to 1.0
    class_to_vec=[]
    
    for i in range(10):
        vec=10*[0.0]
        vec[i]=1.0
        class_to_vec.append(vec)
    
    training_out=[]
    
    for c in training_output_class:
        training_out.append(class_to_vec[c])
    
    
    
    test_out=[]
    
    for c in test_output_class:
        test_out.append(class_to_vec[c])
    
    
    MAX_ITERS = 100000
    
    #print guess
    
    TOL=0.1
    best_error=1e32
    mutate_amount=1.0
    iter=0
    
    while iter < MAX_ITERS:
    
        train_net(nn,training_in,training_out)
        #break
        error=test_net(nn,training_in,training_out)
        
        if error < best_error:
            best_error=error
            print iter,error
    
        #break
       
        if error <= TOL:
            break
             
        iter += 1
    
    
    success=best_error <= TOL
    
    if success:
        print " Success ", " Iters ",iter,"\n"
    
    else:
        print " Failed", " best error=",best_error
    
    
    #test_net_print(nn,training_in,training_out)




import cProfile
cProfile.run("doit()")       