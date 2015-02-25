
# parameters

import world 
import array 
import random
import Tkinter 
import gui 
import  matplotlib.pyplot


POPSIZE      = 200;          # population size      
MAXITER      = 100000;           # maximum iterations
BREEDPROB    = 0.5;          # mutation rate
NELITE       = 10;           # top of population survive
NBREED       = 100;       

do_breed=False


def blank_gene(length):
    g=Gene()  
    g.str=array.array('B',[0] * length)
    return g

def random_gene(length,maxTok):
    g=blank_gene(length)
    for i in range(length):
        g.str[i]=random_token(maxTok)
    return g
    
def mate(a,b):
        length=len(a.str)
        i=random.randint(1,length-1)
        g=Gene()        
        g.str=array.array('B',a.str[0:i]+b.str[i:length])
        return g

def random_token(maxTok):
        return random.randint(0,maxTok)

def mutate(g,maxTok): # randomly replace a character
    length=len(g.str)
    i=random.randint(0,length-1)
    #g2=g.clone()
    g.str[i]=random_token(maxTok)


class Gene:
    
    def clone(self):
        g=Gene()
        g.str=self.str[:]
        return g
 
 
   
    
def breedPopulation(pop):
    newpop=[]
    
    # copy top NELITE to the new population
    for m in pop[0:NELITE]:
        newpop.append(m)

    # create the rest by breeding from the top NBREED 
    for i in range(NELITE,POPSIZE):
        i1 = random.randint(0,NBREED-1)
        i2 = random.randint(0,NBREED-1)
        
        if do_breed and random.random()<BREEDPROB:
            gene=mate(pop[i1],pop[i2])
           
        else: 
            gene=pop[i1].clone()
            mutate(gene,world.World.maxTok)
            
        newpop.append(gene)
 
    return newpop



class Run:
    

    def __init__(self):
       
        
        master = Tkinter.Tk()
        self.frame=Tkinter.Frame(master)
        self.frame.pack()
        
        matplotlib.pyplot.ion()
        matplotlib.pyplot.xlabel("Evaluations")
        matplotlib.pyplot.ylabel("Fitness")
        
        
        b = Tkinter.Button(self.frame, text="RANDOM WORLD", fg="black", command=self.init_world)
        c=0
        b.grid(row=0,column=c)
        c+=1
        b = Tkinter.Button(self.frame, text="RESET GA", fg="black", command=self.ga_init)
        b.grid(row=0,column=c)
        c+=1
        b = Tkinter.Button(self.frame, text="STEP", fg="black", command=self.step)
        b.grid(row=0,column=c)
        c+=1
        b = Tkinter.Button(self.frame, text="RUN (GA)", fg="black", command=self.run_ga)
        b.grid(row=0,column=c)
        c+=1
        b = Tkinter.Button(self.frame, text="RUN (RANDOM)", fg="black", command=self.run_random)
        b.grid(row=0,column=c)
        c+=1
        b = Tkinter.Button(self.frame, text="STOP", fg="black", command=self.stop)
        b.grid(row=0,column=c)
        c+=1
        self.breed_flag= Tkinter.IntVar()
        b = Tkinter.Checkbutton(self.frame, text="BREED", fg="black", variable=self.breed_flag,command=self.breed_func)
        b.grid(row=0,column=c)
        #b.pack()
        c+=1
        b = Tkinter.Button(self.frame, text="PLOT", fg="black", command=self.plot)
        b.grid(row=0,column=c)
 
        gui.init(600,600,10)
        self.canvas = Tkinter.Canvas(self.frame, width=gui.xMax, height=gui.yMax+40)
        self.canvas.grid(row=1,columnspan=c)
        self.run_init()       
        self.init_world()
                                
    def breed_func(self):
        global do_breed
        do_breed = not do_breed
        print " Breed=",self.breed_flag.get(),do_breed
        
    def init_world(self):
        self.world=world.World()
        self.ga_init()
        gui.draw_world_init(self.world, self.canvas)
        
    def run_init(self):
        self.iter=[]
        self.cost=[]
        self.count=0  
        self.best=-1e20
        self.running=False
        
    def ga_init(self): 
        self.pop=[]
        for i in range(POPSIZE):
            self.pop.append(random_gene(self.world.gene_length,self.world.maxTok))
    
        
    def stop(self):
        self.running=False
   
    
    def run_ga(self):
        
        if self.running:
            return
        self.run_init()
        self.running=True
        while self.count < MAXITER and self.running:
            self.step();


    def step_random(self):
        g=random_gene(self.world.gene_length,self.world.maxTok)
        fit=self.world.evaluate(g)
        if fit > self.best:
            text=" evaluations:"+str(self.count)+ "   fitness:"+str(fit) 
            self.iter.append(self.count)
            self.cost.append(fit)   
            self.best = fit
            self.world.evaluate(g, True)
            self.canvas.delete(Tkinter.ALL)
            gui.draw_world(self.world, self.canvas,text)
       # give the GUI a chance to do stuff  
        if (self.count % POPSIZE) == 0:
            self.frame.update()
        self.count += 1
        
        
    def run_random(self):
        self.run_init()
        self.running=True
        while self.count < MAXITER and self.running:
            self.step_random();
           

    def step(self):
        
        for m in self.pop:
            m.fitness=self.world.evaluate(m)
            
        pop = sorted(self.pop, key = lambda x:x.fitness,reverse=True)
    
        p = self.pop[0]
        
        if p.fitness > self.best:
            text=" evaluations:"+str(self.count*POPSIZE)+ "   fitness:"+str(p.fitness) 
            self.iter.append(self.count*POPSIZE)
            self.cost.append(p.fitness)
            self.best = p.fitness
            self.world.evaluate(p, True)
            self.canvas.delete(Tkinter.ALL)
            gui.draw_world(self.world, self.canvas,text)
      
        # give the GUI a chance to do stuff  
        self.frame.update()
              
        self.pop = breedPopulation(pop);
        self.count += 1

    def plot(self):   
        
        matplotlib.pyplot.plot(self.iter,self.cost)
     
      
        
if __name__ == '__main__':

    run=Run()
    
    Tkinter.mainloop() 
    
     


  


