"""
Set of classes to create Neural Nets.
"""


class Neuron:
  # encapsulate a neuron
  # construct a neuron that has n_in inputs
  # 
  def __init__(self,n_in):
    self.n_in=n_in

  def fire(self,input):
    
    assert len(input) == self.n_in
    
    sum=self.weights[self.n_in]    # bias
    for x,w in zip(input,self.weights):
          sum += x*w
    
    if sum > 0.0:
        return 1.0
    else:
        return 0.0
    
  def set_weights(self,weights):
    assert len(weights) == self.n_in+1
    self.weights=weights
    
  def debug(self):
        print self.weights
    
class Layer:
       
    def __init__(self,n_in,n_out):
        
        self.neurons=[]
        for i in range(n_out):
            self.neurons.append(Neuron(n_in))
            
        # self.n_in=n_in
        self.out=n_out*[0.0]
        
    def set_weights(self,neuron,weight):
        self.neurons[neuron].set_weights(weight)
    
    def fire(self,input):
        for i in range(len(self.out)):
            self.out[i]=self.neurons[i].fire(input)
        
        return self.out
    
    
    def debug(self):
        cnt=0
        for neuron in self.neurons:
            print "neuron=",cnt
            neuron.debug()
            cnt+=1
            
    def getNeuron(self,i):
        return self.neurons[i]

class Network2Layer:
    
    def __init__(self,n_in,n_hidden,n_out):
        self.layers=[]
        self.layers.append(Layer(n_in,n_hidden))
        self.layers.append(Layer(n_hidden,n_out))
        #self.n_out=n_out

    def set_weights(self,w):
        for lay in range(len(w)):
            for neuron in range(len(w[lay])):
                self.layers[lay].set_weights(neuron,w[lay][neuron])
    

    def fire(self,input):
    
        for layer in self.layers:
            input=layer.fire(input)
        
        return input
    
    
    def debug(self):
        cnt=0
        for layer in self.layers:
            print "layer=",cnt
            layer.debug()
            cnt+=1
            
    def getLayer(self,i):
        return self.layers[i]
            
            
