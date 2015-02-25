
# parameters

import world 

import Tkinter 
import gui 
import  matplotlib.pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  #, NavigationToolbar2TkAgg
import ga
import subprocess


N_CONSUMERS=10
N_GENERATORS=25

POPSIZE_INIT          = 200          # population size      
MAXITER               = 100000       # maximum iterations
ELITE_PERCENT         = 5           # top of population survive to next generation unchanged  
SELECT_PERCENT        = 20           # top SELECT_PERCENT are used for regeneratio

BREED_PROB_PERCENT    = 50           # probability that we breed 

MUTATE_PERCENT        = 50           # percentage of regen. that we mutate  
MUTATE_TOKENS         = 1          # percentage of the number of tokens mutated
MUTATE_AMOUNT_PERCENT  = 100          # max amount of mutation for each token 




plt=matplotlib.pyplot



class GAFrame:
    
    def __init(self,master):
        pass
        
class Run:
    
   
    def __init__(self):
        
        
       
        self.lines=[]   
        self.running=False
        master = Tkinter.Tk()
        swidth=master.winfo_screenwidth()
        sheight=master.winfo_screenwidth()
        master.geometry("%dx%d+0+0"% (swidth,sheight))
        
                
        self.master=master
        
        
        cmd_frame=Tkinter.Frame(master)
        
        # make the buttons
        frame=self.make_button_frame(cmd_frame)
        frame.pack(side=Tkinter.RIGHT)
         
        frame=self.make_world_frame(cmd_frame)
        frame.pack(side=Tkinter.RIGHT)
         
        #make the sliders     
        frame=self.make_slider_frame(cmd_frame)
        frame.pack(side=Tkinter.RIGHT,fill=Tkinter.X,expand=True)
        
        cmd_frame.pack(side=Tkinter.TOP,fill=Tkinter.X)
        
        # Graph by embeddding a matplotlib plot!
        # matplotlib.pyplot.ion()
        plot_frame=Tkinter.Frame(master)
       
        ww=swidth*0.4
        wh=sheight*0.5
        ww=min(ww,500)
        wh=min(wh,500)
        
        ww1=(swidth-ww)/300
        wh1=(sheight-wh)/300
         
        self.fig = plt.figure()  # figsize=(ww1,wh1))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xscale('log')
        matplotlib.pyplot.xlabel("Evaluations")
        matplotlib.pyplot.ylabel("Cost")
        matplotlib.pyplot.title("Cost of Network")
        
       
       
           
        self.world_canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.world_canvas.show()
        self.world_canvas.get_tk_widget().grid(row=0,column=1)
            
            
        # World canvas   
       
    
       
        self.canvas = Tkinter.Canvas(plot_frame,bg="#777", width=ww,height=wh )
        self.canvas.grid(row=0,column=0)
        
        
        plot_frame.pack(side=Tkinter.BOTTOM)
        self.set_buttons_default()

        self.init_world(ww,wh,10)  
        self.ga_init()
        self.run_init()
  
                      
 
        
    def init_world(self,w=None,h=None,marg=None):
        if w != None:
            gui.init(w,h,marg)
            
        self.world=world.World(self.generator_slider.get(),
                               self.consumer_slider.get())
        self.ga_init()

        #self.mutate_tokens.options(to=self.world.gene_length)
        gui.draw_world_init(self.world, self.canvas)
        self.clear_graph()
            
   
    def make_button_frame(self,container):
        
        frame=Tkinter.Frame(container)
        b = Tkinter.Button(frame, text="RANDOM WORLD", fg="black",command=self.init_world)
        b.grid(row=0,column=0,sticky="WENS")
        self.rand_world=b
#         
#         b = Tkinter.Button(frame, text="RESET GA", fg="black", command=self.ga_init)
#         b.grid(row=1,column=0,sticky="WENS")
#         self.reset_ga=b
        
#         b = Tkinter.Button(frame, text="STEP (GA)", fg="black", command=self.step_ga)
#         b.grid(row=1,column=0,sticky="WENS")
#         self.step_ga_but=b
   
        
        b = Tkinter.Button(frame, text="RUN (GA)", fg="black", command=self.run_ga)
        b.grid(row=2,column=0,sticky="WENS")
        self.run_ga_but=b
   
        b = Tkinter.Button(frame, text="RUN (RANDOM)", fg="black", command=self.run_random)
        b.grid(row=3,column=0,sticky="WENS")
        self.run_random_but=b
        
        b = Tkinter.Button(frame, text="CLEAR GRAPH", fg="black", command=self.clear_graph)
        b.grid(row=4,column=0,sticky="WENS")
        self.clear_graph_button=b
        
        b = Tkinter.Button(frame, text="SNAP SHOT", fg="black", command=self.snap_shot)
        b.grid(row=5,column=0,sticky="WENS")
   
     
#         b = Tkinter.Button(frame, text="STOP", fg="black", command=self.stop)
#         b.grid(row=3,columnspan=2,sticky="WENS")
#         self.stop_run=b
#    
        
   
        return frame

    def snap_shot(self):
        self.canvas.postscript(file="GA.eps")
        
        child = subprocess.Popen("gv GA.eps&", shell=True) # convert eps to jpg with ImageMagick
#         child.wait()
        
     
#         child = SP.Popen("mogrify -format jpg circles.eps", shell=True) # convert eps to jpg with ImageMagick
#         child.wait()
        
    def set_all_buttons(self,state):
                 
                 self.rand_world.config(state=state)
#                  self.step_ga_but.config(state=state)
#                  self.reset_ga.config(state=state)
                 self.run_ga_but.config(state=state)
                 self.run_random_but.config(state=state)
                 self.clear_graph_button.config(state=state)
                 self.consumer_slider.config(state=state)
                 self.generator_slider.config(state=state)
                 
#                  self.stop_run.config(state=state)

    def set_buttons_default(self):
            self.set_all_buttons(Tkinter.NORMAL)
#             self.step_ga.config(state=state)
#             self.reset_ga.config(state=state)
#             self.step_ga.config(state=state)
#             self.run_ga.config(state=state)
#             self.run_random.config(state=state)
#             self.stop_run.config(state=state)
            
    def set_button_active(self,but):
         but.config(state=Tkinter.ACTIVE)
        
    def  set_button_normal(self,but):
         but.config(state=Tkinter.NORMAL)
      
      
    def make_slider_frame(self,master):

        scale_wid=5
        frame=Tkinter.Frame(master)
        i=0
        # frame.grid_columnconfigure(1,weight=4) 
        lab=Tkinter.Label(frame,text="Population size:",anchor="e")
        lab.grid(row=i,column=0,sticky="SE")
        self.pop_slider = Tkinter.Scale(frame,  
                                        from_=2, to=1000,orient=Tkinter.HORIZONTAL,width=scale_wid)
        self.pop_slider.set(POPSIZE_INIT)
        
        self.pop_slider.grid(row=i,column=1)
        i+=1
        
        lab=Tkinter.Label(frame,text="Elite: Top % of Population kept unchanged:",anchor="e")
        lab.grid(row=i,column=0,sticky="SE")
        self.elite_percent = Tkinter.Scale(frame, 
                                           from_=0, to=100,orient=Tkinter.HORIZONTAL,width=scale_wid)
        self.elite_percent.set(ELITE_PERCENT)
        self.elite_percent.grid(row=i,column=1)
        i+=1
        
        lab=Tkinter.Label(frame,text="Select: % of Population for creating new population:",anchor="e")
        lab.grid(row=i,column=0,sticky="SE")
        self.select_percent = Tkinter.Scale(frame,
                                             from_=0, to=100,orient=Tkinter.HORIZONTAL,width=scale_wid)
        self.select_percent.set(SELECT_PERCENT)
        self.select_percent.grid(row=i,column=1)
        i+=1
        
        lab=Tkinter.Label(frame,text="Percentage of selected to be mated:",anchor="e")
        lab.grid(row=i,column=0,sticky="SE")
        self.breed_prob_percent = Tkinter.Scale(frame, 
                                                from_=0, to=100,orient=Tkinter.HORIZONTAL,width=scale_wid)
        self.breed_prob_percent.set(BREED_PROB_PERCENT)
        self.breed_prob_percent.grid(row=i,column=1)
        i+=1
        
        
        lab=Tkinter.Label(frame,text="Percentage of new genes to be mutated:",anchor="e")
        lab.grid(row=i,column=0,sticky="SE") 
        self.mutate_percent = Tkinter.Scale(frame,
                                              from_=0, to=100,orient=Tkinter.HORIZONTAL,width=scale_wid)
        self.mutate_percent.set(MUTATE_PERCENT)
        self.mutate_percent.grid(row=i,column=1)
        i+=1
       
        lab=Tkinter.Label(frame,text="Mutate: Maximum amount per token (%)")
        lab.grid(row=i,column=0,sticky="SE")
        self.mutate_amount_percent = Tkinter.Scale(frame,
                                                     from_=0, to=100,orient=Tkinter.HORIZONTAL,width=scale_wid)
        self.mutate_amount_percent.set(MUTATE_AMOUNT_PERCENT)
        self.mutate_amount_percent.grid(row=i,column=1)
        i+=1
       
        lab=Tkinter.Label(frame,text="Number of tokens in the gene to mutate:",anchor="e")
        lab.grid(row=i,column=0,sticky="SE")
        self.mutate_tokens = Tkinter.Scale(frame,  
                                           from_=0, to=50,orient=Tkinter.HORIZONTAL,width=scale_wid)
        self.mutate_tokens.set(1)
        self.mutate_tokens.grid(row=i,column=1)
        i+=1
       
        return frame
                  
      
    def make_world_frame(self,master):

        scale_wid=5
        frame=Tkinter.Frame(master)
        i=0
        # frame.grid_columnconfigure(1,weight=4) 
        lab=Tkinter.Label(frame,text="Number of Consumers:",anchor="e")
        lab.grid(row=i,column=0,sticky="SE")
        self.consumer_slider = Tkinter.Scale(frame,  
                                        from_=1, to=25,orient=Tkinter.HORIZONTAL,width=scale_wid)
        self.consumer_slider.set(N_CONSUMERS)
        
        self.consumer_slider.grid(row=i,column=1)
        i+=1
        
        lab=Tkinter.Label(frame,text="Number of generator sites:",anchor="e")
        lab.grid(row=i,column=0,sticky="SE")
        self.generator_slider = Tkinter.Scale(frame, 
                                           from_=1, to=25,orient=Tkinter.HORIZONTAL,width=scale_wid)
        self.generator_slider.set(N_GENERATORS)
        self.generator_slider.grid(row=i,column=1)
        i+=1
               
        return frame

    def clear_graph(self):
        
        for line in self.lines:
            line.remove()
            
        line,=self.ax.plot([1,100], [0,0], ',')
        self.lines=[line]  
        self.plot()
        
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
            self.pop.append(ga.random_gene(self.world.gene_length,self.world.maxTok))
        
    def stop(self):
        self.running=False
        self.set_buttons_default()
        
    def run_ga(self):
     
        if self.running:
            self.stop()
            return
        
        
        self.set_all_buttons(Tkinter.DISABLED)
        self.set_button_active(self.run_ga_but)
        self.ga_init()
        self.run_init()
        self.running=True
        while self.count < MAXITER and self.running:
            self.step_ga();
         

    def step_random(self):
        
        g=ga.random_gene(self.world.gene_length,self.world.maxTok)
        fit=self.world.evaluate(g)
        if fit > self.best or (self.count % 1000) == 0 :
            text=" evaluations:"+str(self.count)+ "   fitness:"+str(fit) 
            self.iter.append(self.count+1)
            self.cost.append(-fit)   
            self.best = fit
            self.world.evaluate(g, True)
            self.canvas.delete(Tkinter.ALL)
            gui.draw_world(self.world, self.canvas,text)
            self.plot()
                
       # give the GUI a chance to do stuff  
        if (self.count % self.pop_size) == 0:
            self.master.update()
        self.count += 1
        
        
    def run_random(self):
       
        if self.running:
            self.stop()
            return
        
        
        self.set_all_buttons(Tkinter.DISABLED)
        self.set_button_active(self.run_random_but)
        self.ga_init()
        self.run_init()
        self.running=True
      
        while self.count < MAXITER and self.running:
            self.step_random();
           

    def step_ga(self):
        
        for m in self.pop:
            m.fitness=self.world.evaluate(m)
            
        pop = sorted(self.pop, key = lambda x:x.fitness,reverse=True)
    
        p = self.pop[0]
        
        if p.fitness > self.best or (self.count % 10) == 0 :
            text=" evaluations:"+str(self.count*self.pop_size)+ "   fitness:"+str(p.fitness) 
            self.iter.append(self.count*self.pop_size+1)
            self.cost.append(-p.fitness)
            self.best = p.fitness
            self.world.evaluate(p, True)
            self.canvas.delete(Tkinter.ALL)
            gui.draw_world(self.world, self.canvas,text)
            self.plot()
        

        # give the GUI a chance to do stuff  
        self.master.update()
          
          
        elite_percent=self.elite_percent.get()        
        select_percent=self.select_percent.get()
        breed_prob_percent=self.breed_prob_percent.get()
        mutate_percent=self.mutate_percent.get()
        mutate_tokens=self.mutate_tokens.get()
        mutate_amount_percent=self.mutate_amount_percent.get()
      
         
              
        self.pop = ga.breedPopulation(pop,world.World.maxTok,
                                      elite_percent,
                                      select_percent,
                                      breed_prob_percent,
                                      mutate_percent,
                                      mutate_tokens,
                                      mutate_amount_percent)
        self.count += 1

    def plot(self):   
     #   print "PLOT"
        if len(self.lines) <= 1 :
            self.fig.canvas.draw()
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
    
     


  


