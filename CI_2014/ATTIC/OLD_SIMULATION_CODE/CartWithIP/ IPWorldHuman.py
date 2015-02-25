#
#   Simulation of an inverted pendulum
#
# This example demonstrates how to use the Simulation environment
# A simple neural net is used to control the inverted pendulum.
# Networks are created and tested using random weights until a successful one is found    
#  (maybe never!!!)

import simulation
import math
import gui
import ip
import sys
import brain
import rungakutta
import pickle


# Load previously saved brain as first attempt.
load_brain=False

# neural net layer definitions
N_IN=4
N_OUT=2
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
TARGET_FIT=30   

# Size of the display window  
SCREEN_W=1000
SCREEN_H=200


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
    Return true if pendulum has fallen over 
    """
    return  ip.getAngle() > MAX_ANGLE or ip.getAngle() < MIN_ANGLE

def reap1(ip):
    """
    Return true if pendulum has fallen over or has moved too far from x=0
    """
    return abs(ip.getX() > MAX_X) or  ip.getAngle() > MAX_ANGLE or ip.getAngle() < MIN_ANGLE
    
    
def fitness(ip):
    """
    Simple fitness is just the time
    """
    return ip.time


class IPWorld:
    """
    Container to simulate the inverted pendulum.
    Collaborates with the simulation.
    See methods for details about the contract.
    """
    
    
    def __init__(self,dt):
      
    
        self.dt=dt           # time between gui updates
        self.ip=ip.InvertedPendulum(length = 1.5, mass = 1., mass_cart = .1,dt=0.001)     # inverted pendulum physical model
        self.ip.reset(INITIAL_ANG)        # starting angle
            
        self.rk=rungakutta.RungeKutta(self.ip.state,0,0.01,self.ip)     # time step engine     
        
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
        
        
         # --- use keypresses to determine control
        force=0.0
        keyinput = gui.get_pressed()  
        if keyinput[gui.keys.K_LEFT]:
            force -= 1.0

        if keyinput[gui.keys.K_RIGHT]:
            force+= 1.0
            
        # Using difference of 2 outputs for symmetry (I don't know if this is a good idea!)      
        self.ip.setForce(force)
        self.rk.step(self.dt)
    
        # print self.inp
           
        if reap(self.ip):
            
            self.rk.reset()
            self.ip.reset(INITIAL_ANG)
         
        
    def draw(self,screen):
        """
        Called by the simulation to display the current state.
        This is decoupled from the step method to allow faster simulations with less frequent screen
        updates.
        """ 
       
        wid=gui.dim_window[0]
        hei=gui.dim_window[1]
        
        length=self.ip.l
        scale=hei/length/3.0
        
        x1=wid/2.0+self.ip.getX()*scale
        if x1 > wid*.8:
            x1 =wid*.8
        if x1 < -wid*.8:
            x1 = -wid*.8
            
        y1=hei*.6

        ang=self.ip.getAngle()
        x2=x1+scale*math.sin(ang)*length
        y2=y1+scale*math.cos(ang)*length
        
        # print x1,y1,x2,y2
        col=(255,0,0)
        thick=3
        gui.draw_line(screen,x1,y1,x2,y2,col,thick)
        col=(0,255,0)
        gui.fill_circle(screen,x2,y2,12,col)
        
        col=(0,0,255)
        thick=20
        gui.draw_line(screen,x1-20,y1,x1+20,y1,col,thick)
        
        col=(0,255,255)
        
        
        
        str2 = "Frame rate: %6.4f    [ + | - ] : [speed up | slow down ] " % (sim.frameskipfactor/float(sim.slowMotionFactor))
         
        #, self.inp[1], self.inp[2] ,self.inp[3]
        gui.draw_string(screen,str2,(10,hei-20),col,16)
        
        

dt=0.05      # time step for gui and control rate in secs
title="Inverted Pendulum"
ipWorld=IPWorld(dt)
sim=simulation.Simulation(ipWorld,title)
sim.run()