# GA to evolve "Hello World!"
# using roullette wheel selection

import sys
import random
import array
import copy

POPSIZE       = 100            # population size	  
MAXITER       = 10000          # maximum iterations
CROSSOVERPROB = 0.5            # Prob that we create by crossover breeding (otherwise clone + mutate) 
MUTATEPROB    = 0.1	           # mutation rate of crossover offspring

target="Hello World!"
size=len(target)

low_char=32
hi_char=121

class Gene:
    def __init__(self,string):
        self.string=copy.copy(string)
        self.fitness=None    

def randomChar():
    return chr(random.randint(low_char,hi_char))

def seed():
    string=array.array('c')
    for i in xrange(size):
        string.append(randomChar())
    return string

def evaluate1(string):  # number correct
        summ=0
        for a,b in zip(string,target):
            if a == b:
                summ += 1
        return summ
        
        
def mutate1(a):     # randomly replace a character
        i=random.randint(0,size-1)
        a[i]=randomChar()

    
def evaluate2(string):    #  sum of diff in char codes
        summ=size*(hi_char-low_char)
        for a,b in zip(string,target):
                summ -= abs(ord(a)-ord(b))
        return summ
        
def mutate2(a):    #  add/subtract 1 from the character code
        i=random.randint(0,size-1)
        ic = ord(a[i])
        im=random.randint(0,1)
        ic=ic + 2*im -1
        if ic >hi_char:
            ic=hi_char
        if ic <low_char:
            ic=low_char
        a[i]=chr(ic)

mutate=mutate2
evaluate=evaluate2      
  
def mate(a,b):
    i=random.randint(1,size-1)
    ret = a[0:i]+b[i:size]
    #print ret
    return ret



def clone(string):
    return copy.deepcopy(string)

# Roullette wheel selection
# probability of selection for a gene is fitness/SUMofPopulation_fitnesses
# I am too embaressed to explain how this code works
class RouletteWheel:
    
    # initialize roullette wheel with a population 
    def __init__(self,pop):
        self.totfit=0.0
        self.totfitsofar=[]
        self.pop=pop

        for m in pop:
            self.totfit += m.fitness
            self.totfitsofar.append(self.totfit)

    # select a gene using roullette wheel
    def select(self):
        r = random.random()*self.totfit
        # print r,self.totfit        
        #
        #  The following is a terrible bit of coding     
        #  please use a balanced binary tree to make this run faster

        for v,m in zip(self.totfitsofar,self.pop):
            if v >= r:
                return m

        print "OOOOOPS"
    
    
    
# create a new population
def breedPopulation(wheel):
    
    newpop=[]

    for i in range(POPSIZE):     
        dad=wheel.select()   # select using the wheel
        
        if random.random() < CROSSOVERPROB:   # should we breed ?
            mum=wheel.select()
            child=Gene(mate(dad.string,mum.string))   # yes: then do it   
            if random.random() < MUTATEPROB:              # should we mutate ?
                mutate(child.string)
        else:
            child=Gene(clone(dad.string))  
            mutate(child.string)                       # no: then just clone the parent
                       
        newpop.append(child)                          # add to new population
    
            
    return newpop


if __name__ == '__main__':

    # set the best fitness possible as the target
    target_fitness=evaluate(target)

    # create inital population with random genes
    pop=[]

    for i in range(POPSIZE):
        pop.append(Gene(seed()))



    # loop until we find the target
    count=0    # keep a count of how many generations in takes

    while  count< MAXITER:

        fitmax=-1e32
        
        # evaluate the fitness of all genes in the population
        for m in pop:
            m.fitness=evaluate(m.string)
            if m.fitness > fitmax:
                fitmax=m.fitness
                best=m
        

        print count*POPSIZE,best.string.tostring(),fitmax
        
        if  fitmax >=  target_fitness:
            break
        
        # set up the roullette wheel
        wheel=RouletteWheel(pop)

        # create a new population by breeding etc.
        # use the wheel to select parents
        pop = breedPopulation(wheel);

        count += 1
        