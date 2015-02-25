# converted to java  and then to python by p.j.leonard
# based  on C++ code found at 
# http://www.codeproject.com/KB/recipes/BP.aspx?msg=2809798#xx2809798xx


import math
import random
import copy
import pickle

"""
multilayer neural network
"""

                    

def sigmoid(x):
        if x < -100.0:     # avoid math.exp(x) blowing up
            return 0.0      
        return 1.0 / (1.0 + math.exp(-x))
    
def atan(x):
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
    
    def __init__(self,size,func=None,weight=None):
        """
        Create a multi layer network
        
        Number of nodes in each layer is define by size
            size[0] is the number of inputs
            size[n] number of neurons in layer n
        
        
        func is an array of activation functions
            if this is None the activation defaults to sigmoid.
        
        weight can be used to initialize the weights of the NN
            if weight is None random values are assigned to the weights. 
        
        """
        
        sz=size
        #//    set no of layers and their sizes
        self.num_layer = len(sz)
        
        if func == None:
            func=[]
            func.append(None)
            for _ in range(self.num_layer):
                func.append(sigmoid)
                
        self.layer_size = []   # new int[num_layer];
        self.func=func
        for  i in range(self.num_layer):
            self.layer_size.append(sz[i])

 
        #//	allocate memory for output of each neuron
        self.out = [] # new float[num_layer][];
        for  i in range(self.num_layer):  
            self.out.append([]);
            a=self.out[i]
            for _ in range(self.layer_size[i]):
                a.append(0.0)


        if weight == None:
            self.weight=[]
            self.weight.append([])
            
            for i in range(1,self.num_layer):  
                self.weight.append([])
                a=self.weight[i]
                for j in range(self.layer_size[i]):
                    a.append([])
                    r=a[j]
                    for _ in range(self.layer_size[i - 1]):
                        r.append(randomSeed())
                    r.append(randomSeed())
        else:
            self.weight=weight
    
    
    def ffwd(self,x):
        """
        input: x  list of input values
        
        returns:   list of output values.
        
        """
        
        
        #	assign content to input layer
        for  layer in range(self.layer_size[0]):
            self.out[0][layer] = x[layer]       # output_from_neuron(layer,j) Jth neuron in Ith Layer

        #	assign output(activation) value 
        #	to each neuron using sigmoid func
        
        for layer in range(1,self.num_layer):         #  For each layer
            for j in range(self.layer_size[layer]):   #  For each neuron in current layer
                sum = 0.0;
                for k  in range(self.layer_size[layer - 1]):                     # For input from each neuron in preceeding layer
                    sum += self.out[layer - 1][k] * self.weight[layer][j][k];	# Apply weight to inputs and add to sum
                
                sum += self.weight[layer][j][self.layer_size[layer - 1]];	    	# Apply bias
                self.out[layer][j] = self.func[layer](sum);				            # Apply sigmoid function
    
        return self.out[self.num_layer - 1];
    
 
 
#------------------ More advanced functionality (you can ignore this) ---------------------------------------------------
      
    def resize_inputs(self,nIn):
        
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
        
    def clone(self):
        clone=FeedForwardBrain(self.layer_size,self.func,self.weight)
        return clone

    
    def mutate(self,amount):    
        """ 
        mutate *all* the weights by a random amount.
        param: amount: range of mutation  (in the range +-amount/2)
        """
         
        # for all layers with inputs
        for i in range(1,self.num_layer):
            a=self.weight[i]  
            # for all neurons in the layer
            for j in range(self.layer_size[i]):            
                r=a[j]
                for k in range(self.layer_size[i-1]+1):
                    r[k]=r[k]+randomSeed()*amount
                    
    def dist(self,brain):    
        """
         sqrt(sum of diff weights squared)         
        :param brain: compare with
        """
         
        sum=0.0
        # for all layers with inputs
        for i in range(1,self.num_layer):
            a=self.weight[i] 
            b=brain.weight[i]
             
            # for all neurons in the layer
            for j in range(self.layer_size[i]):            
                ra=a[j]
                rb=b[j]
                for k in range(self.layer_size[i-1]+1):
                    sum += (ra[k]-rb[k])**2
                    
        return math.sqrt(sum) 

    def output(self):
        return self.out[self.num_layer - 1];
    
    
    def input(self):
        return self.out[0];
    
    
    # mean square error
    def mse(self,tgt): 
        mse = 0.0;
        for i in range(self.layer_size[self.num_layer - 1]):
            mse += (tgt[i] - self.out[self.num_layer - 1][i]) * (tgt[i] - self.out[self.num_layer - 1][i]);
        
        return mse / 2.0;
                   
    def random_mutate(self,amount):    
        
        for i in range(1,self.num_layer):
            a=self.weight[i]  
            for j in range(self.layer_size[i]):            
                r=a[j]
                k=random.randint(0, self.layer_size[i-1]+1)
                z=random.randint(0, (self.layer_size[i-1]+1))
                while k < z:
                    r[k]=r[k]+randomSeed()*amount
                    k=k+1 
            
            