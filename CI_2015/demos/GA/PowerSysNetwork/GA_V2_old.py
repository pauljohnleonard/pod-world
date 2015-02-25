
# parameters

import world 
import array 
import random
import Tkinter 
import gui 
import  matplotlib.pyplot


POPSIZE_INIT          = 200          # population size      
MAXITER               = 100000       # maximum iterations
ELITE_PERCENT         = 10           # top of population survive to next generation unchanged  
SELECT_PERCENT        = 50           # top SELECT_PERCENT are used for regeneratio

BREED_PROB_PERCENT    = 50           # probability that we breed 

MUTATE_PERCENT        = 50           # percentage of regen. that we mutate  
MUTATE_TOKENS_PERCENT = 100          # percentage of the number of tokens mutated
MUTATE_AMOUNT_PERCENT  = 100          # max amount of mutation for each token 




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

def random_token(maxTokVal):
        return random.randint(0,maxTokVal)
    
def mutate_token(tok,maxTokVal,amount):
        tok=int(tok+(random.random()-0.5)*maxTokVal*amount)
        tok=max(0,tok)
        tok=min(maxTokVal,tok)
        return tok
    
def mutate(g,maxTokVal,n_toks,amount): # randomly replace a character
    """
    Mutate n token
    amount is between 0 and 1 and determines the possible range 0 none 1 up to maxTokVal
    """
    
    length=len(g.str)
  
 
    for _ in range(n_toks):
        i=random.randint(0,length-1)
       # print i
    #g2=g.clone()
        g.str[i]=mutate_token(g.str[i],maxTokVal,amount)


class Gene:
    
    def clone(self):
        g=Gene()
        g.str=self.str[:]
        return g
 
 
   
    
def breedPopulation(pop,elite_percent,select_percent,breed_prob_percent,mutate_percent,mutate_tokens,mutate_amount_percent):
    pop_size=len(pop)
    newpop=[]
    
    nelite=int(len(pop)*elite_percent/100.0)
    nelite=max(0,nelite)
    
    nselect=int(len(pop)*select_percent/100.0)
    nselect=max(nselect,1)
    
    # copy top NELITE to the new population
    for m in pop[0:nelite]:
        newpop.append(m)

    # create the rest by breeding from the top NBREED 
    for i in range(nelite,pop_size):
        i1 = random.randint(0,nselect-1)
      
        
        if random.random() < breed_prob_percent/100.0:
            i2 = random.randint(0,nselect-1)
            gene=mate(pop[i1],pop[i2])
        else: 
            gene=pop[i1].clone()
            
        if random.random() < mutate_percent/100.0:
            mutate(gene,world.World.maxTok,mutate_tokens,mutate_amount_percent/100.0)
            
        newpop.append(gene)
 
    return newpop

plt=matplotlib.pyplot



class GAFrame:
    
    def __init(self,master):
        pass
        
class Run:
    
    def make_button_frame(self,container):
        
        frame=Tkinter.Frame(container)
        b = Tkinter.Button(frame, text="RANDOM WORLD", fg="black", command=self.init_world)
        c=0
        b.grid(row=0,column=c)
        c+=1
        
        
        b = Tkinter.Button(frame, text="RESET GA", fg="black", command=self.ga_init)
        b.grid(row=0,column=c)
        c+=1
        
        b = Tkinter.Button(frame, text="STEP (GA)", fg="black", command=self.step_ga)
        b.grid(row=0,column=c)
        c+=1
        
        b = Tkinter.Button(frame, text="RUN (GA)", fg="black", command=self.run_ga)
        b.grid(row=0,column=c)
        c+=1
        
        b = Tkinter.Button(frame, text="RUN (RANDOM)", fg="black", command=self.run_random)
        b.grid(row=0,column=c)
        c+=1
        
        b = Tkinter.Button(frame, text="STOP", fg="black", command=self.stop)
        b.grid(row=0,column=c)
 
        

        return frame


    def make_slider_frame(self,master):

        frame=Tkinter.Frame(master)
        self.pop_slider = Tkinter.Scale(frame, label="Population size", from_=1, to=1000,orient=Tkinter.HORIZONTAL)
        self.pop_slider.set(POPSIZE_INIT)
        self.pop_slider.pack(fill=Tkinter.X)
        
        
        self.elite_percent = Tkinter.Scale(frame, label="Elite: Top % of Population kept unchanged", from_=0, to=100,orient=Tkinter.HORIZONTAL)
        self.elite_percent.set(ELITE_PERCENT)
        self.elite_percent.pack(fill=Tkinter.X)
        
        self.select_percent = Tkinter.Scale(frame, label="Select from top % of Population for creating rest of new population", from_=0, to=100,orient=Tkinter.HORIZONTAL)
        self.select_percent.set(SELECT_PERCENT)
        self.select_percent.pack(fill=Tkinter.X)
        
        self.breed_prob_percent = Tkinter.Scale(frame, label="Percentage of selected to be mated ", from_=0, to=100,orient=Tkinter.HORIZONTAL)
        self.breed_prob_percent.set(BREED_PROB_PERCENT)
        self.breed_prob_percent.pack(fill=Tkinter.X)
        
        
        self.mutate_percent = Tkinter.Scale(frame, label="Percentage of new genes to be mutated %",  from_=0, to=100,orient=Tkinter.HORIZONTAL)
        self.mutate_percent.set(MUTATE_PERCENT)
        self.mutate_percent.pack(fill=Tkinter.X)

        self.mutate_amount_percent = Tkinter.Scale(frame, label="Mutate: Maximum amount per token (%)",  from_=0, to=100,orient=Tkinter.HORIZONTAL)
        self.mutate_amount_percent.set(MUTATE_AMOUNT_PERCENT)
        self.mutate_amount_percent.pack(fill=Tkinter.X)
      
        self.mutate_tokens = Tkinter.Scale(frame, label="Number of tokens in the gene to mutate /"+str(world.World.maxTok), 
                                           from_=0, to=world.World.maxTok,orient=Tkinter.HORIZONTAL)
        self.mutate_tokens.set(1)
        self.mutate_tokens.pack(fill=Tkinter.X)
        return frame
    
    def __init__(self):
       
        self.lines=[]   
        self.running=False
        master = Tkinter.Tk()
        
        frame=self.make_button_frame(master)
        frame.pack()
        
       
        frame=self.make_slider_frame(master)
        frame.pack(fill=Tkinter.X)

        matplotlib.pyplot.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        matplotlib.pyplot.xlabel("Evaluations")
        matplotlib.pyplot.ylabel("Fitness")
         
            
        gui.init(600,600,10)
        self.canvas = Tkinter.Canvas(master, width=gui.xMax, height=gui.yMax+40)
        self.canvas.pack()
        
     
        self.init_world()
        
  
                      
    def plot_tog(self):
    #    print "DO PLOT"
        self.plot()
        
#                   
#     def breed_func(self):
#         global do_breed
#         do_breed = not do_breed
#         print " Breed=",self.breed_flag.get(),do_breed
        
    def init_world(self):
        self.world=world.World()
        self.ga_init()
        gui.draw_world_init(self.world, self.canvas)
        
        for line in self.lines:
            line.remove()
            
        self.lines=[]
        
        
    def run_init(self):
        self.iter=[]
        self.cost=[]
        self.count=0  
        self.best=-1e20
        self.running=False

        line, = self.ax.plot([], [], '-')
        self.lines.append(line)
               
    def ga_init(self): 
        self.pop=[]
        self.pop_size=self.pop_slider.get()
        for i in range(self.pop_size):
            self.pop.append(random_gene(self.world.gene_length,self.world.maxTok))
    
    def stop(self):
        self.running=False
   
    def run_ga(self):
     
            
        if self.running:
            return
        
        
        self.run_init()
        self.running=True
        while self.count < MAXITER and self.running:
            self.step_ga();
         

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
            if self.plot_flag.get():
                self.plot()
                
       # give the GUI a chance to do stuff  
        if (self.count % self.pop_size) == 0:
            self.frame.update()
        self.count += 1
        
        
    def run_random(self):
        self.gkey='-'
  
        self.run_init()
        self.running=True
        while self.count < MAXITER and self.running:
            self.step_random();
           

    def step_ga(self):
        
        for m in self.pop:
            m.fitness=self.world.evaluate(m)
            
        pop = sorted(self.pop, key = lambda x:x.fitness,reverse=True)
    
        p = self.pop[0]
        
        if p.fitness > self.best:
            text=" evaluations:"+str(self.count*self.pop_size)+ "   fitness:"+str(p.fitness) 
            self.iter.append(self.count*self.pop_size)
            self.cost.append(p.fitness)
            self.best = p.fitness
            self.world.evaluate(p, True)
            self.canvas.delete(Tkinter.ALL)
            gui.draw_world(self.world, self.canvas,text)
            if self.plot_flag.get():
                self.plot()

        # give the GUI a chance to do stuff  
        self.frame.update()
          
          
        elite_percent=self.elite_percent.get()        
        select_percent=self.select_percent.get()
        breed_prob_percent=self.breed_prob_percent.get()
        mutate_percent=self.mutate_percent.get()
        mutate_tokens=self.mutate_tokens.get()
        
        mutate_amount_percent=self.mutate_amount_percent.get()
      
         
              
        self.pop = breedPopulation(pop,elite_percent,select_percent,breed_prob_percent,mutate_percent,mutate_tokens,mutate_amount_percent)
        self.count += 1

    def plot(self):   
     #   print "PLOT"
        if len(self.lines) == 0 :
            return
        
        
        self.lines[-1].set_data(self.iter,self.cost)
        
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
 
        
#         matplotlib.pyplot.plot()
     
      
        
if __name__ == '__main__':

    run=Run()
    print " RUNINNG"
    Tkinter.mainloop() 
    
     


  


