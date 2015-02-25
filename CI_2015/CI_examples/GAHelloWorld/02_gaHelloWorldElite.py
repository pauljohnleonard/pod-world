# GA hello world
# Selection using ranking with ellitism

import sys
import random
import array
import copy

"""
Parameters to be tweaked
"""

elitePercent=5               # Percentage copied to next generation
selectPercent=50             # Top 50% available for selection

POPSIZE      = 100           # population size	  
MAXITER      = 1000          # maximum iterations
CROSSOVERPROB= 0.5           # Fraction of new population created by crossover breeding
MUTATEPROB   = 0.5  	     # mutation rate of breed genes


## End of tweakable parameters

NELITE       = int((POPSIZE*elitePercent)/100);           # top of population survive
NSELECT       = int((POPSIZE*selectPercent)/100);           # how many are bred

secret="Hello World!"
size=len(secret);

low_char=32
hi_char=121

class Gene:
    def __init__(self,string):
        self.string=string
        self.fitness=None    
        
    def funcPrint(self):
        print self.string, self.fitness
        
             
def randomChar():
    return chr(random.randint(low_char,hi_char))

def seed():
    string=array.array('c')
    for i in xrange(size):
        string.append(randomChar())
    return string

def evaluate1(string):   # number correct
    sum=0
    for a,b in zip(string,secret):
        if a == b:
            sum += 1
    return sum



def clone(string):
    return copy.deepcopy(string)


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
 
def evaluate2(string):    # sum of diff in char codes
    sum=0
    for a,b in zip(string,secret):
            sum -= abs(ord(a)-ord(b))
    return sum
   
    
# creat the next generation
def newPopulation():
    newpop=[]
    
    # copy top NELITE to the new population
    for m in pop[0:NELITE]:
        newpop.append(m)

    # create the rest by breeding/cloning+mutating from the top NSELECT 
    for i in range(NELITE,POPSIZE):
   
        i1 = random.randint(0,NSELECT-1)
        
        if random.random() < CROSSOVERPROB:            # create by breeding
            i2 = random.randint(0,NSELECT-1)
            gene=Gene(mate(pop[i1].string,pop[i2].string))
            if random.random() < MUTATEPROB:
                mutate(gene.string)
                
        else:
            gene=Gene(clone(pop[i1].string))            # just clone
            mutate(gene.string)                         #' always mutate cloned
            
        newpop.append(gene)

            
    return newpop


if __name__ == '__main__':

    mutate=mutate2
    evaluate=evaluate2
    
    target_fitness=evaluate(secret)

    pop=[]

    for i in range(POPSIZE):
        pop.append(Gene(seed()))

    count=0    

    while  count< MAXITER*POPSIZE:

        for m in pop:
            m.fitness=evaluate(m.string)
            count += 1

        pop = sorted(pop, key = lambda x:x.fitness,reverse=True)
    
        print count,pop[0].string.tostring(),pop[0].fitness  
        
        if pop[0].fitness >=  target_fitness:
            break

        pop = newPopulation();
       

  


