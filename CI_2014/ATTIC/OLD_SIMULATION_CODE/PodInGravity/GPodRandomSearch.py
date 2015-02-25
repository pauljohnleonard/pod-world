#
#   Simulation of an inverted pendulum
#
# This example demonstrates how to use the Simulation environment
# A simple neural net is used to control the inverted pendulum.
# Networks are created and tested using random weights untill a successful one is found    
#

import simulation
import math
import gui
import gravitypod
import sys
import brain
import pickle


# Load previously saved brain as first attempt.
load_brain=False

# neural net layer definitions
N_IN=4
N_OUT=3
N_HIDDEN=4

sz=[N_IN,N_HIDDEN,N_OUT]


# Limits to measure failure (
MAX_X=6.0
MAX_ANGLE=math.pi+1.0
MIN_ANGLE=math.pi-1.0

# initial angle 
INITIAL_ANG=math.pi-0.3

# arbitrary scaling for NN output!!!
FORCE_FACT=50.0

# look for 1 minute of success
TARGET_FIT=60   

# Size of the display window  
SCREEN_W=1000
SCREEN_H=800
X_INIT=SCREEN_W/2
Y_INIT=SCREEN_H/2

def saveBrain(brain):
    """
    Saves a brain
    """
    
    fout=open("brain.dat",'w')
    pickle.dump(brain,fout)
    fout.close()

def loadBrain():
    """
    Loads a saved brain
    """
    fin=open("brain.dat",'r')
    b=pickle.load(fin)
    fin.close()
    return b

def createBrain():
    """
    Create a random network of the given size
    """
    return brain.FeedForwardBrain(sz)
      
      
def reap(ip):
    """
    Return true if pod is out of bounds 
    """
    return ip.state.x < 0   or  ip.state.x > SCREEN_W or ip.state.y > SCREEN_H or ip.state.y < 0
    
def fitness(ip):
    """
    Simple fitness is just the time
    """
    return ip.state.age

def init_pod(pod):
    """
    put pod in center of the screen
    """
    pod.init()
    pod.state.x=X_INIT
    pod.state.y=Y_INIT
    pod.state.ang=math.pi


class PodWorld:
    """
    Container to simulate the gravity pod.
    Collaborates with the simulation.
    See methods for details about the contract.
    """
    
    
    def __init__(self,dt):
      
    
        self.dt=dt                          # time between gui updates
        self.ip=gravitypod.GravityPod()     # gravity podphysical model
        
        
        init_pod(self.ip)
        
        if load_brain:
            print " Loading a saved brain "
            self.net=load_brain()
        else:
            print " Creating a random brain"
            self.net=createBrain()            # initial randoim network
        
        self.inp=6*[0]
        self.generation=0
        self.fit_max=0.0
        
    def dimensions(self):
        """
        returns size of the graphical area in pixels.
        """
        return SCREEN_W,SCREEN_H
    
    def start(self):
        """
        Call once at the very start 
        """
        pass
        
    def step(self):
        """
        Called repeatedly by the simulation.   
             
        Advances the physical model by a single step.
        
        If pendulum is out of bounds
            create a new brain  and reset the simulation.
        
        If fitness has reached target value.
           save brain and stop the simulation
       
        """
        
        # copy state of IP for input into the network
        ss=self.ip.state
        self.inp[0] = ss.x-X_INIT
        self.inp[1] = ss.y-Y_INIT
        self.inp[2] = ss.dxdt
        self.inp[3] = ss.dydt
        self.inp[4] = ss.ang-math.pi
        self.inp[5] = ss.dangdt
        
        # print self.inp        
                
        out=self.net.ffwd(self.inp)  
        
        self.ip.step(out,self.dt)
        
        # print self.out
           
        if reap(self.ip):
            self.generation +=1
            fit=fitness(self.ip)  
            if fit> self.fit_max:
                self.fit_max=fit
                      
            self.net=createBrain()        
            init_pod(self.ip)
            
        if fitness(self.ip) > TARGET_FIT:
            print " Target fitness has been achieved... savi8ng brain "
            saveBrain(self.net)
            sim.stop()

            
        
    def draw(self,screen):
        """
        Called by the simulation to display the current state.
        This is decoupled from the step method to allow faster simulations with less frequent screen
        updates.
        """ 
       
        self.ip.draw(screen)
        
        wid=gui.dim_window[0]
        hei=gui.dim_window[1]
        
       
        
        col=(0,255,255)
        
        str2 = "Time: %3.1f " % self.ip.state.age
        str2+= "Best: %3.1f " %self.fit_max
        str2+= "Generation: %3d " % self.generation
        str2+= "Work: %5d " % sim.ticks
        
        gui.draw_string(screen,str2,(20,10),col,16)
        
        str2 = "x: %5.2f "  % (self.inp[0])
        str2+= "y: %5.2f " % self.inp[1]
        str2+= "dxdt: %5.2f " % self.inp[2]
        str2+= "dydt: %5.2f " %self.inp[3]
        str2+= "Phi: %5.2f " % self.inp[4]
        str2+= "dphidt: %5.2f " %self.inp[5]
        
        gui.draw_string(screen,str2,(20,25),(255,255,0),16)
        
        str2 = "Frame rate: %6.4f    [ + | - ] : [speed up | slow down ] " % (sim.frameskipfactor/float(sim.slowMotionFactor))
         
        #, self.inp[1], self.inp[2] ,self.inp[3]
        gui.draw_string(screen,str2,(10,hei-20),col,16)
        
        

dt=0.05      # time step for gui and control rate in secs
title="Gravity Pod"
podWorld=PodWorld(dt)
sim=simulation.Simulation(podWorld,title)
sim.run()