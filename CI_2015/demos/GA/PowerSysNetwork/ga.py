import array 
import random

def blank_gene(length):
    """
    @param length     number of tokens in the gene
    return an empty gene
    """
    
    g=Gene()  
    g.str=array.array('B',[0] * length)
    return g

def random_gene(length,maxTokVal):
    """
    @param length     number of tokens in the gene
    @param maxTokVal  tokens are random integers between 0 and maxTokVal
    
    return a random gene
    """
    
    g=blank_gene(length)
    for i in range(length):
        g.str[i]=random_token(maxTokVal)
    return g
    
def mate(a,b):
    """
    Return a new gene created by cross over of the gens a and b
    cross over is a random point within the gene
    """
    length=len(a.str)
    i=random.randint(1,length-1)
    g=Gene()        
    g.str=array.array('B',a.str[0:i]+b.str[i:length])
    return g

def random_token(maxTokVal):
        return random.randint(0, maxTokVal)
    
def mutate_token(tok, maxTokVal, amount):
        tok = int(tok + 2 * (random.random() - 0.5) * maxTokVal * amount)
        tok = max(0, tok)
        tok = min(maxTokVal, tok)
        return tok
    
def mutate(g,maxTokVal,n_toks,amount): # randomly replace a character
    """
    Mutate n token
    amount is between 0 and 1 and determines the possible range 0 none 1 up to maxTokVal
    """
    
    length=len(g.str)

    
    for _ in range(n_toks):
        i=random.randint(0,length-1)
        g.str[i]=mutate_token(g.str[i],maxTokVal,amount)


class Gene:
    """
    Class to hold a gene
    """
    def clone(self):
        g=Gene()
        g.str=self.str[:]
        return g
 
 
   

def breedPopulation(pop,maxTok,
                    elite_percent,
                    select_percent,
                    breed_prob_percent,
                    mutate_percent,
                    mutate_tokens_percent,
                    mutate_amount_percent):
    
    
    pop_size=len(pop)    # print i
    #g2=g.clone()
    newpop=[]
    
    nelite=int(len(pop)*elite_percent/100.0)
    nelite=max(0,nelite)
    
    nselect=int(len(pop)*select_percent/100.0)
    nselect=max(nselect,1)
    

    # copy top NELITE to the new population
    for m in pop[0:nelite]:
        newpop.append(m)

    # create the rest by breeding from the top NBREED 
    for _ in range(nelite,pop_size):
        mum = random.randint(0,nselect-1)
        
        if random.random() < breed_prob_percent/100.0:
            dad = random.randint(0,nselect-1)
            gene=mate(pop[mum],pop[dad])
        else: 
            gene=pop[mum].clone()
            
        if random.random() < mutate_percent/100.0:    # print i
    #g2=g.clone()
            mutate(gene,maxTok,mutate_tokens_percent,mutate_amount_percent/100.0)
            
        newpop.append(gene)
 
    return newpop
