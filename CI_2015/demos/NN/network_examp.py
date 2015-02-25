#  This program shows you how to use a simple 2 layer feed forward network.

# The code that implements the network is in the following module.
from neuralnet import * 
   
   
# create a network with 2 layers
# 2 inputs 
# 2 hidden 
# 1 output.
 
net=Network2Layer(2,2,1)
  
  
# store the weights in a list of list of lists
# first list is layers
# next inner list is neurons in that layer
# inner most is a list of weights for that neuron
 
# e.g. some randomish weights
"""
              out
           /   |   \
         /     |    \
        1       -2    1
       /        \      \   
      hid0      hid1    1
      / | \     /  |  \
     1  1  0   -2  -2  1
    /   |   \   |   |   |
in0    in1   1 in0 in1   1

"""
 
weights=[[[2,2,-1],[-3,-3,2]],    # input  -> hidden weights
          [[3,-2,-2]]]           # hidden -> output weights
    
    
net.set_weights(weights)
    
net.debug()
    
print " X1 X2    OUTPUT"
for x1 in range(2):
    for x2 in range(2):
            input=[x1,x2]
            output=net.fire(input)
            print " %2.1f %2.1f  %2.1f" % (x1,x2,output[0])
