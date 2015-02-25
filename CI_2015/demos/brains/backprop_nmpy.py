#
# multilayer neural network with backprop training
#     
# based  on C++ code found at 
# http://www.codeproject.com/KB/recipes/BP.aspx?msg=2809798#xx2809798xx
# converted to java  and then to python by p.j.leonard
#
# Uses numpy for vector products. Still not as fast as JAVA or C.

import math
import random
import copy
import numpy



def sigmoid(x):
        if x < -100.0:        #  stops function blowing up !!!!
            return 0.0
    
        return 1.0 / (1.0 + math.exp(-x))
    
def randomSeed():
    return 0.5 - random.random()

    
class BackPropBrain:
  

    def __init__(self,sz, beta=.001, alpha=40.):
        """ Create a neural net
            sz is  list that defines the number neurons in each layer
            beta is the learning rate
            alpha is the momentum
            """ 
        
        self.beta = beta
        self.alpha = alpha

        #//    set no of layers and their sizes
        self.num_layer = len(sz)
        self.layer_size = []   # new int[num_layer];

        for  i in range(self.num_layer):
            self.layer_size.append(sz[i])

 
        #//    allocate memory for output of each neuron
        self.out = [] # new float[num_layer][];
        for  i in range(self.num_layer):  
            self.out.append([]);
            a=self.out[i]
            for _ in range(self.layer_size[i]):
                a.append(0.0)
            a.append(1.0)
            self.out[i]=numpy.array(a)
        
        self.delta = []
        for  i in range(self.num_layer):  
            self.delta.append([]);
            a=self.delta[i]
            for _ in range(self.layer_size[i]):
                a.append(0.0)
            self.delta[i]=numpy.array(a)


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
                a[j]=numpy.array(r)
            self.weight[i]=numpy.array(self.weight[i])
                
        self.prevDwt=[]
        self.prevDwt.append([])
        
        for i in range(1,self.num_layer):  
            self.prevDwt.append([])
            a=self.prevDwt[i]
            for j in range(self.layer_size[i]):
                a.append([])
                r=a[j]
                for _ in range(self.layer_size[i - 1]):   
                    r.append(0.0)
                r.append(0.0)
                a[j]=numpy.array(r)
       
         
        
    def clone(self):
        clone=BackPropBrain(self.layer_size,self.alpha,self.beta)
        clone.weight=copy.deepcopy(self.weight)
        return clone
            
    def mutate(self,amount):    
        for i in range(1,self.num_layer):
            a=self.weight[i]  
            for j in range(self.layer_size[i]):            
                r=a[j]
                for k in range(self.layer_size[i-1]+1):
                    r[k]=r[k]+randomSeed()*amount
                    
 
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
   

    #  feed forward one set of input
    def ffwd(self,x):
        
        for i,xa in enumerate(x):
            self.out[0][i]=xa
         
        #    assign output(activation) value 
        #    to each neuron usng sigmoid func
        
        for i in range(1,self.num_layer):         #  For each layer
            for j in range(self.layer_size[i]):   #  For each neuron in current layer
                sum = numpy.dot(self.out[i - 1], self.weight[i][j])
                #for k  in range(self.layer_size[i - 1]):                     # For input from each neuron in preceeding layer
                #    sum += self.out[i - 1][k] * self.weight[i][j][k];    # Apply weight to inputs and add to sum
                
                sum += self.weight[i][j][self.layer_size[i - 1]]            # Apply bias
                self.out[i][j] = sigmoid(sum);                              # Apply sigmoid function
    
        return self.out[self.num_layer - 1];
    
    #    back-propagate errors from output.
    #    modify weights
    def bpgt(self,x, tgt1):
        
       
        tgt=copy.copy(tgt1)
        tgt.append(0)
        tgt=numpy.array(tgt)
        
        #    update output values for each neuron
        self.ffwd(x);

        #    find delta for output layer
        #for i in range(self.layer_size[self.num_layer - 1]):  
        #    self.delta[self.num_layer - 1][i] = self.out[self.num_layer - 1][i] * \
        #            (1 - self.out[self.num_layer - 1][i]) * (tgt[i] - self.out[self.num_layer - 1][i])
        self.delta[self.num_layer - 1]= self.out[self.num_layer - 1] * \
                    (1.0 - self.out[self.num_layer - 1]) * (tgt - self.out[self.num_layer - 1])
        

        #   find delta for hidden layers    
        for i in range(self.num_layer-2,0,-1) : 
            nn=len(self.delta[i + 1])-1
            for  j  in range(self.layer_size[i]):
              
                #print numpy.shape(self.delta[i + 1][:nn]),numpy.shape(self.weight[i + 1][:,j])
                sum=numpy.dot(self.delta[i + 1][:nn],self.weight[i + 1][:,j])
              
                #sum = 0.0            
                #for k in range(self.layer_size[i + 1]):
                #    sum += self.delta[i + 1][k] * self.weight[i + 1][k][j]
                self.delta[i][j] = self.out[i][j] * (1 - self.out[i][j]) * sum;
                
                
          
         
        #    apply momentum ( does nothing if alpha=0 )
        for i in range(1,self.num_layer):
            for j in range(self.layer_size[i]):
                self.weight[i][j] += self.alpha * self.prevDwt[i][j]
                
                self.weight[i][j][self.layer_size[i - 1]] += self.alpha * self.prevDwt[i][j][self.layer_size[i - 1]]
            
        #    adjust weights using steepest descent    
        for i in range(1,self.num_layer):
            for j in range(self.layer_size[i]):
                #for  k in range(self.layer_size[i - 1]):
                self.prevDwt[i][j] = self.beta * self.delta[i][j] * self.out[i - 1]
                self.weight[i][j] += self.prevDwt[i][j]
                
                self.prevDwt[i][j][self.layer_size[i - 1]] = self.beta * self.delta[i][j]
                self.weight[i][j][self.layer_size[i - 1]] += self.prevDwt[i][j][self.layer_size[i - 1]]
    
        return self.mse(tgt)
            
            
   