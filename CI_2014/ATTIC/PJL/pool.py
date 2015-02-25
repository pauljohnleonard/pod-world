"""

Shows how to use a Pool for implementing a GA.

Pool is fixed size.

Pool expects the functions

seed()
mutate(a)
mate(a,b)

to exist and operate on the representation 

The class Gene is a holder for the actual representation and the fitness.

"""

import sys
import random
import array
import copy

"""

Holder for the gene  and it's fitness

"""
class GeneWrapper:
    def __init__(self,gene):
        self.gene=gene      #  representation (can be anything you want) 
        self.fitness=None       #  fitness (once calculated)
        
    def __str__(self):
        return str(self.gene)+" Fitness "+ str(self.fitness)
 




class Pool:
 
    """
    A Pool maintains a list of Genes limit by size.
    
    It also has a create method to create new Genes.
    See methods for details.
    Initially the pool is empty
    """
    
    def __init__(self,size,factory,breed_prob=0.0,seed_prob=0.0):
        
        """
        Create a pool with no initial population
        """
        self.list=[]
        self.size=size
        self.factory=factory
        self.breed_prob=breed_prob
        self.seed_prob=seed_prob
        
        
    def add(self,gene,fit):
        """
        If the pool is not full then the gene is added to the population.
        Otherwise:
        If the gene fitness is greater than any other in the pool then it is added.
        and the least fit is removed
        """
        
        n=len(self.list)
        for i in range(n):
            if self.list[i].fitness < fit:
                wrap=GeneWrapper(gene)
                wrap.fitness=fit
                self.list.insert(i,wrap)
                if n > self.size-1:
                    self.list.pop()
                return
            
        if n < self.size:
            wrap=GeneWrapper(gene)
            wrap.fitness=fit
            
            self.list.append(wrap)
            
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
        if len(self.list) < (self.size) or random.random() < self.seed_prob:    
            print "RANDOM"
            
            return self.factory.seed()
        
        # randomly depending on BREED_PROB mate 2 existing genes.
        elif  random.random() < self.breed_prob:
            print "BREED"
            mum=self._select()
            dad=self._select()
            string=self.factory.mate(mum.gene,dad.gene)
            return string
                
        #other wise return a mutated version of a random gene from the pool 
        else:
            print "MUTATE"
            gg=self._select()
            #print gg
            wrap=self._select()   
            #print wrap  
            return self.factory.mutate(wrap.gene)
            
    
    def _select(self):
        
        if len(self.list) == 0:
            return self.list[0]
            
        id=random.randint(0,len(self.list)-1)
        return self.list[id] 
    
    def __str__(self):
        ret ="---POOL --------------------------\n"
        for g in self.list:
            ret  += str(g) + "\n" 
            
        return ret
            
