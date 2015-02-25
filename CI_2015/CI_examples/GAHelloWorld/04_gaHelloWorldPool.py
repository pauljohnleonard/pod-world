"""

Shows how to use a Pool for implementing a GA.

Pool is fixed size.

Pool expects the functions

seed()
mutate(a)
mate(a,b)

to create and operate on the representation (gene)

The class Gene is a holder for the actual representation and the fitness.

"""

import sys
import random
import array
import copy

secret="Hello World!"
size=len(secret);

# POOL creation scheme.
SEED_PROB=0.0              # probability a new thing is created from nothing
BREED_PROB=0.0             # prob that new entity is from breeding 
MUTATE_PROB=0.0            # prob that a breed gene is mutated
# Otherwise randomly mutate any existing gene. 

POOL_SIZE=10


low_char=32
hi_char=121

"""

Holder for the gene string and it's fitness

"""
class Gene:
    def __init__(self,string):
        self.string=string      #  representation (can be anything you want) 
        self.fitness=None       #  fitness (once calculated)
        
    def __str__(self):
        return str(self.string)+" Fitness "+ str(self.fitness)
           
def randomChar():
    return chr(random.randint(low_char,hi_char))

def seed():
    string=array.array('c')
    for i in xrange(size):
        string.append(randomChar())
    return string


def mate(a,b):
    i=random.randint(1,size-1)
    ret = a[0:i]+b[i:size]
    return ret



def mutate1(a): # randomly replace a character
    i=random.randint(0,size-1)
    a[i]=randomChar()

def mutate2(a):    # add/subtract 1 from the character code
    i=random.randint(0,size-1)
    ic = ord(a[i])
    im=random.randint(0,1)
    ic=ic + 2*im -1
    if ic >hi_char:
        ic=hi_char
    if ic <low_char:
        ic=low_char
    a[i]=chr(ic)
    

def evaluate1(string):   # number correct
    sum=0
    for a,b in zip(string,secret):
        if a == b:
            sum += 1
    return sum

def evaluate2(string):    # sum of diff in char codes
    sum=0
    for a,b in zip(string,secret):
            sum -= abs(ord(a)-ord(b))
    return sum


evaluate=evaluate2
mutate=mutate2


class Pool:
 
    """
    A Pool maintains a list of Genes limit by size.
    
    It also has a create method to create new Genes.
    See methods for details.
    Initially the pool is empty
    """
    
    def __init__(self,size):
        
        """
        Create a pool with no initial population
        """
        self.list=[]
        self.size=size
        
        
        
    def add(self,gene):
        """
        If the pool is not full then the gene is added to the population.
        Otherwise:
        If the gene fitness is greater than any other in the pool then it is added.
        and the least fit is removed
        """
        
        n=len(self.list)
        for i in range(n):
            if self.list[i].fitness < gene.fitness:
                self.list.insert(i,gene)
                if n > self.size-1:
                    self.list.pop()
                return
            
        if n < self.size:
            self.list.append(gene)
            
    def create(self):     
        """ create a new brain.
            If pool is not full create a random brain.
            Otherwise either   (probabilities are determined by SEED_PROB and BREED_PROB)
                 create by breeding randomly from the pool.   
                 OR create by cloning then mutation
                 OR create a random gene 
            
        """
    
        # if list is not full OR randomly depending on SEED_PROB
        # create a random gene.
        if len(self.list) < (self.size) or random.random() < SEED_PROB:    
            #print "RANDOM"
            gene=Gene(seed())
            return gene
        
        # randomly depending on BREED_PROB mate 2 existing genes.
        elif  random.random() < BREED_PROB:
            #print "BREED"
            mum=self._select()
            dad=self._select()
            string=mate(mum.string,dad.string)
            if random.random() < MUTATE_PROB:
                mutate(string)
            return Gene(string)
                
        #other wise return a mutated version of a random gene from the pool 
        else:
            #print "MUTATE"
            gene=copy.deepcopy(self._select())     
            mutate(gene.string)
            return gene
            
    
    def _select(self):
        
        if len(self.list) == 0:
            return self.list[0]
            
        id=random.randint(0,len(self.list)-1)
        return self.list[id] 
    
    def funcPrint(self):
        print "-----------------------------"
        for g in self.list:
            print g
            
        
pool=Pool(POOL_SIZE)

target_fitness=evaluate(secret)

cnt=0

max_eval=100000

while cnt< max_eval:
    gene=pool.create()      #   Create a new gene from the pool
    gene.fitness=evaluate(gene.string)
    
    pool.add(gene)
    best_gene=pool.list[0]
    #pool.funcPrint()
    print cnt,": ",best_gene
    if best_gene.fitness == target_fitness:
        print "DONE IT"            
        break
    cnt = cnt+1

            
        