
import simulation
import pods

import world
import gui


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

        #  ----  Just to demonstrate what information is available to use for input to the control
        if True:   #   keyinput[gui.keys.K_x]:
            # -------  This code prints out all the available information about the state of the pod
        
            for attr, value in pod.state.__dict__.iteritems():
                print str(attr)+ " "+ str(value),
            print
        

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


# Creates an "instance" of a CursorControl
controller=CursorController()


# create a CarPod with 
# --- no snesors (empty list)  
# --- it will use control

sensors=[]       #  no sensors
pod=pods.SpriteCar()
pod.addSensors(sensors) 
pod.setController(controller)
pod.set_image("car_PJ.png")

# pod=CarPod([],control,(255,255,0))
# we need to pass a list of pods to the world when we create it

podlist=[pod]     #  list with just one element  

    
# world definition file
#worldFile="carCircuit.world"
worldFile="./worlds/carCircuit.world"
# Time step
dt=0.1   # go slow   

# create  the world
myWorld=world.World(worldFile,dt,podlist)

sim=simulation.Simulation(myWorld,"My Title")
sim.run()