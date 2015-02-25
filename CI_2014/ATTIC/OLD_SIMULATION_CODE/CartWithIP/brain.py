
import math
import random
import copy
import pickle

"""

multilayer neural network.

This version is designed for effeciency so is less object oriented.

The bias input in implemented by adding an extra weight to each set of inputs.

The weights are stored as an 3 dimensional array   [layers][neurons_in_layer][weights_into_neuron]  
  
e.g.  3 inputs  2 hidden neurons 1 output

The weights might be
             in-hidden               hidden-out
weights=[ [[1 2 3 0],[3 4 5 -1]] ,   [[8,9,2]]  ]

"""


def step(x):
    """
    Threshold step function
    """
    
    if x>0:
        return 1
    
    return 0                    

def sigmoid(x):
    """ 
    transfer function with an output range 0 to 1
    """
    
    if x < -100.0:     # avoid math.exp(x) blowing up
            return 0.0      
    return 1.0 / (1.0 + math.exp(-x))
    
def atan(x):
    """ 
    transfer function with an output range -1 to 1
    """

    if x < -100.:
            return -1.0
        
    if x > 100.:
            return 1.0
              
    ee=math.exp(-x)
    return (1.0 -ee) / (1.0 + ee)
    
    
def randomSeed():
    """
    Random number between -0.5  and 0.5
    """
    return 0.5 - random.random()



    
class FeedForwardBrain:
    """
    Basic feedforward neural net  
    """
    
    def __init__(self,size=None,func=None,weight=None):
        """
        Create a multi layer network
        
        Number of nodes in each layer is define by size
            size[0] is the number of inputs
            size[n] number of neurons in layer n
        
        
        func is an array of activation functions (for each layer)
            if this is None the activation defaults to sigmoid.
        
        weight can be used to initialize the weights of the NN
            in this case size can be None

            otherwise if weight is None random values are assigned to the weights using size 
             
            
         Example for 2 inputs 2 hidden and 1 output
         
         size=[2,2,1]
         
           
        """
      
      
        self.layer_size = []
        if weight != None:
            self.weight=weight
            self.layer_size.append(len(weight[0][0])-1)
            for i in range(len(self.weight)):
                self.layer_size.append(len(weight[i]))              
        else:
            for  i in range(len(size)):
                self.layer_size.append(size[i])
       
       # print self.layer_size                         
        
        self.num_layer=len(self.layer_size)
        
        if func == None:
            func=[]
            for _ in range(self.num_layer):
                func.append(sigmoid)
        self.func=func
        
      

 
        #//	allocate memory for output of each neuron
        self.out = [] # new float[num_layer][];
        for  i in range(self.num_layer):  
            self.out.append([]);
            a=self.out[i]
            for _ in range(self.layer_size[i]):
                a.append(0.0)


        if weight == None:
            self.weight=[]
            
            for i in range(self.num_layer-1):  
                layer=[]
                for _ in range(self.layer_size[i+1]):
                    w=[]
                    for _ in range(self.layer_size[i]):
                        w.append(randomSeed())
                    w.append(randomSeed())
                    layer.append(w)
                self.weight.append(layer)
        
    
    def ffwd(self,x):
        """
        input: x  list of input values
        
        returns:   list of output values.
        
        """
        
        
        #	assign content to input layer
        for  i in range(self.layer_size[0]):
            self.out[0][i] = x[i]       # output_from_neuron(layer,j) Jth neuron in Ith Layer

        #	assign output(activation) value 
        #	to each neuron using sigmoid func
        
        for layer in range(self.num_layer-1):         #  For each layer
            for j in range(self.layer_size[layer+1]):   #  For each neuron in current layer
                sum = 0.0;
                for k  in range(self.layer_size[layer]):                     # For input from each neuron in preceeding layer
                    sum += self.out[layer][k] * self.weight[layer][j][k];	# Apply weight to inputs and add to sum
                
                sum += self.weight[layer][j][self.layer_size[layer]];	    	# Apply bias
                self.out[layer+1][j] = self.func[layer](sum);				    # Apply transfer function
    
        return self.out[self.num_layer - 1];
    

    def copyWeights(self):
        """
        Return a copy of the weights
        """
        
        return copy.deepcopy(self.wieghts)
    
    def clone(self):
        """
        Create a new brain which is the same as this one.
        """
        
        clone=FeedForwardBrain(self.layer_size,self.func,self.weight)
        return clone
 
 
#------------------ More advanced functionality (you can ignore this) ---------------------------------------------------
      
    def resize_inputs(self,nIn):
        
        
        """
         Add extra inputs to the network 
        """
        
        assert nIn > self.layer_size[0]
        
        for _ in range(nIn-self.layer_size[0]):    
            self.out[0].append(0.0)
                
        for a in self.weight[1]:
            wLast=a.pop()
            a.append(0.0)                 
            for _ in range(nIn-self.layer_size[0]-1):    
                a.append(0.0)
            a.append(wLast)
            
        if self.layer_size[0]<nIn:
            self.layer_size[0]=nIn

    
def mutate1(brain,amount):    
        """ 
        mutate *all* the weights by a random amount.
        amount: range of mutation is    amount*0.5
        """
         
        # for all layers with inputs
        for i in range(1,brain.num_layer):
            a=brain.weight[i]  
            # for all neurons in the layer
            for j in range(brain.layer_size[i]):            
                r=a[j]
                for k in range(brain.layer_size[i-1]+1):
                    r[k]=r[k]+randomSeed()*amount
                    
def dist(brain1,brain2):    
        """
        WARNING UNTESTED --- might be useful for implement Niches
        
        WARNING NO ERROR CHECKING (brains must be same topology)
        
         sqrt(sum of diff weights squared)         
        compares brain1 and brain2 by calculating Euclidean distance between weight vectors
        
        """
         
        sum=0.0
        # for all layers with inputs
        for i in range(1,brain1.num_layer):
            a=brain1.weight[i] 
            b=brain2.weight[i]
             
            # for all neurons in the layer
            for j in range(brain1.layer_size[i]):            
                ra=a[j]
                rb=b[j]
                for k in range(brain1.layer_size[i-1]+1):
                    sum += (ra[k]-rb[k])**2
                    
        return math.sqrt(sum) 
    
    
    
    
                   
def mutate2(brain,amount):    
        
        """
        Only mutate a random section of each set of inputs 
        """
        
        for i in range(1,brain.num_layer):
            a=brain.weight[i]  
            for j in range(brain.layer_size[i]):            
                r=a[j]
                k=random.randint(0, brain.layer_size[i-1]+1)
                z=random.randint(0, (brain.layer_size[i-1]+1))
                while k < z:
                    r[k]=r[k]+randomSeed()*amount
                    k=k+1 
            
            