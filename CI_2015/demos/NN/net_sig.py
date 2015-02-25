import math
    
    
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
    
active_func = sigmoid

class Neuron:
        # encapsulate a neuron
        # construct a neuron that has n_in inputs
        # 
        def __init__(self, n_in):
            self.n_in = n_in
        
        def fire(self, input):
            
            assert len(input) == self.n_in
            
            sum = self.weights[self.n_in]    # bias
            for x, w in zip(input, self.weights):
                sum += x * w
           
            return active_func(sum)
            
        def set_weights(self, weights):
            assert len(weights) == self.n_in + 1
            self.weights = weights
            
        def debug(self):
                print self.weights

        
class Layer:
           
        def __init__(self, n_in, n_out):
            
            self.neurons = []
            for i in range(n_out):
                self.neurons.append(Neuron(n_in))
                
            # self.n_in=n_in
            self.out = n_out * [0.0]
            
        def set_weight(self, neuron, weight):
            self.neurons[neuron].set_weights(weight)
        
        def fire(self, input):
            for i in range(len(self.out)):
                self.out[i] = self.neurons[i].fire(input)
            
            return self.out
        
        
        def debug(self):
            cnt = 0
            for neuron in self.neurons:
                print "neuron=", cnt
                neuron.debug()
                cnt += 1

                

class Network2Layer:
    
    def __init__(self,n_in,n_hidden,n_out):
        self.layers=[]
        self.layers.append(Layer(n_in,n_hidden))
        self.layers.append(Layer(n_hidden,n_out))
        #self.n_out=n_out

    def set_weights(self,layer,neuron,weight):
        self.layers[layer].set_weight(neuron,weight)
    

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
            
            
if __name__ == "__main__":        
    net=Network2Layer(2,2,1)
    
    net.set_weights(0,0,[1,1,-1.5])
    net.set_weights(0,1,[-2,-2,1])
    net.set_weights(1,0,[2,2,-1])
    
    net.debug()
    
    print " X1 X2    OUTPUT"
    for x1 in range(2):
        for x2 in range(2):
                input=[x1,x2]
                output=net.fire(input)
                print " %2.1f %2.1f  %2.1f" % (x1,x2,output[0])
