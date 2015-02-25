# GA to evolve "Hello World!"
# using roullette wheel selection

import sys
import random
import array
import copy

POPSIZE       = 1000           # population size	  
MAXITER       = 100            # maximum iterations
CROSSOVERPROB = .5             # Prob that we create by crossover breeding (otherwise clone + mutate) 
MUTATEPROB    = 0.5	           # mutation rate of crossover offspring

target="Hello World!"
size=len(target)

class Gene:
    def __init__(self,string):
        self.string=copy.copy(string)
        self.fitness=None    

def randomChar():
    return chr(random.randint(32,121))

def seed():
    string=array.array('c')
    for i in xrange(size):
        string.append(randomChar())
    return string

def evaluate(string):
    sum=0.0
    for a,b in zip(string,target):
        if a == b:
            sum += 1.0
    return sum

def mate(a,b):
    i=random.randint(1,size-1)
    ret = a[0:i]+b[i:size]
    #print ret
    return ret


def mutate(a):
    i=random.randint(0,size-1)
    a[i]=randomChar()


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

        fitmax=0.0
        
        # evaluate the fitness of all genes in the population
        for m in pop:
            m.fitness=evaluate(m.string)
            if m.fitness > fitmax:
                fitmax=m.fitness
                best=m
        

        print count,best.string.tostring(),fitmax
        
        if  fitmax >=  target_fitness:
            break
        
        # set up the roullette wheel
        wheel=RouletteWheel(pop)

        # create a new population by breeding etc.
        # use the wheel to select parents
        pop = breedPopulation(wheel);

        count += 1
        