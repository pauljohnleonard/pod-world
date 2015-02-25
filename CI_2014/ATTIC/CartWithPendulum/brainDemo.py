"""Demo shows how to use the brain module.
"""

import brain
    
# 3 input 2 hidden 2 outputs
guess=[ [[1, 2, 3, 0],[3, 4, 5, -1]] ,   [[8,9,2],[-4,-5,-6]]  ]
    
net=brain.FeedForwardBrain(weight=guess)

#  apply an input 
out=net.ffwd([.1,.2,-.3])
    
print out
    
guess=[ [[1, 2, 3, 0],[3, 4, 5, -1]] ,  [[-4,-5,-6],[8,9,2]]  ]
    
net.setWeights(guess)
print net.ffwd([.1,.2,-.3])
    
    
guess=[[[1.,2.,3.]]  ]  
net=brain.FeedForwardBrain(weight=guess)
print net.weight
brain.mutate1(net,1.0)

print net.weight