import pool
import random
import array
import copy

secret="Hello World!"
size=len(secret);

low_char=32
hi_char=121

class Factory:          
    def randomChar(self):
        return chr(random.randint(32,121))
    
    def seed(self):
        string=array.array('c')
        for i in xrange(size):
            string.append(self.randomChar())
        return string
    
    def mate(self,a,b):
        i=random.randint(1,size-1)
        ret = a[0:i]+b[i:size]
        return ret
    
    def mutate(self,a): # randomly replace a character
        b=copy.deepcopy(a)
        i=random.randint(0,size-1)
        b[i]=self.randomChar()
        return b

def evaluate(gene):   # number correct
        sum=0
        for a,b in zip(gene,secret):
            if a == b:
                sum += 1
        return sum
 

     
factory=Factory()     
pool=pool.Pool(size=10,factory=factory,breed_prob=.5,seed_prob=0.1)
    
target_fitness=evaluate(secret)
    
cnt=0
    
max_eval=100000
    
while cnt< max_eval:
        gene=pool.create()      #   Create a new gene from the pool
        print gene
        fit=evaluate(gene)
        
        pool.add(gene,fit)
        best_str=pool.list[0]
        #pool.funcPrint()
        print cnt,": ",best_str
        if fit == target_fitness:
            print "DONE IT"            
            break
        cnt = cnt+1
    
                
            