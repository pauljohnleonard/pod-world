
"""
Example that prints the truth table for a NN

NOte the brain.py uses 1 as the bais input  (not -1 in the notes)

"""

import brain 

#  2 inputs 2 layers

# layer 1
#     X1   X2    1      output     
#     -1   -1  0.5         Y1
#     1    1   -1.5        Y2

# layer 2
#     Y1  Y2     1
#      1   1    -0.5       output
#


# weight array has the following format
# weight[layer][neuron_out][neuron_in]

brain=brain.FeedForwardBrain(weight=[[[-1.0,-1.0,0.5],[1.0,1.0,-1.5]],
                                      [[1.0,1.0,-0.5]] 
                                      ],
                             func=[brain.step,brain.step])



for x1 in range(2):
    for x2 in range(2):
        input=[x1,x2]
        output=brain.ffwd(input)
        print x1,x2,output
        
