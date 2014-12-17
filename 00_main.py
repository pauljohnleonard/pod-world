"""
Simple example:
create a car and run it into a wall!
"""

from pod import pods,world
import math


# world (car track) definition file
worldFile="worlds/carCircuit.world"

# create  the world
myWorld=world.World(worldFile)  

#Create a pod 
# Note that the world is responsible for setting the initial state of the pod
pod=pods.CarPod(myWorld)


while True:
    
    pod.control.up=.1
    pod.control.left=.1
    
    # perform a single time step of the car.
    pod.step()
    
    # the state should change (look at the console)
    print pod.state  
    
    if pod.state.collide:   # We have crashed!
        break;   

