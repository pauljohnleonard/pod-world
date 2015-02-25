
import sys
sys.path.append('..')
import simulation
import pods

import world
import gui
import math
import time
import fontmanager

# Example of a user controller
# This defines the class
class CursorController:

    # all controller must implement process
    # this will get called each time step of the simulation
    # it returns a "control" object which is used to control the pod
    
    def process(self,pod,dt):

                
        # what happens here is up to you
        # This example looks at  key press to set the control

        control=pods.Control()
        keyinput = gui.get_pressed()    

        # print the sensor information
        for  sensor in pod.sensors:
             
             print sensor.name ,sensor.val, sensor.wall
             
    
        # --- use keypresses to determine control
        if keyinput[gui.keys.K_LEFT]:
            control.left=.4

        if keyinput[gui.keys.K_RIGHT]:
            control.right=.4

        if keyinput[gui.keys.K_UP]:
            control.up=1

        if keyinput[gui.keys.K_DOWN]:
            control.down=1

        return control




# If you want to draw onto the screen then you need to create a class
# that has a postDraw(self,screen) function

class Painter:   # use me to display stuff
    
    def __init__(self):
        self.preDraw=None       # define this function to draw on top!
        self.fontMgr = fontmanager.cFontManager(((None, 24), (None, 48), ('arial', 24)))
        self.last_time=time.time()
        self.last_ticks = 0
        
    def postDraw(self,screen):
       
        
        tot_ticks=sim.ticks
        ticks=tot_ticks-self.last_ticks
        
        tot_time=time.time()
        
        delta=tot_time-self.last_time
        ticks_per_sec=ticks/delta
        
        self.last_time=tot_time
        self.last_ticks=tot_ticks
                
        
        tickRate="%8.1f" % ticks_per_sec
        
        str1=' ticks:'+ str(sim.ticks) +\
             ' ticks/sec:'+tickRate+"    "
                                                   
       # print str1
        Y=20
        X=20
        self.fontMgr.Draw(screen, None, 24,str1,(X,Y), (0,255,0) )
        
        
   
        

# Creates an "instance" of a CursorControl
controller=CursorController()


# create a CarPod with 
# --- it will use control




ang_ref=math.pi/4.0      # 45 degs
sensorRange=500.0        # range (1 is nominally a pixel)
sLeft=pods.Sensor(ang_ref,sensorRange,"sensorL")
sRight=pods.Sensor(-ang_ref,sensorRange,"sensorR")
sensors=[sLeft,sRight]

  
pod=pods.SpriteCar()
pod.addSensors(sensors)
pod.setController(controller)
pod.set_image("car_PJ.png")


# pod=CarPod([],control,(255,255,0))
# we need to pass a list of pods to the world when we create it

podlist=[pod]     #  list with just one element  

    
# world definition file
#worldFile="carCircuit.world"
worldFile="worlds/carCircuit.world"
# Time step
dt=0.1  

# create  the world
myWorld=world.World(worldFile,dt,podlist)

sim=simulation.Simulation(myWorld,"My Title")

# use myPainter in the simulation
myPainter=Painter()
sim.setPainter(myPainter)


sim.run()