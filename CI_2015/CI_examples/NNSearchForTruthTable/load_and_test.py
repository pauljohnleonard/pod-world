# create a NeuralNet that we will try to optimise for the following training data

# XOR training data

import brain


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
        
        
training_in=[[0.,0.],[0.,1.],[1.,0.],[1.,1.]]
training_out=[[0.],[1.],[1.],[0.]]

nn=brain.loadBrain()

test_net_print(nn,training_in,training_out)

