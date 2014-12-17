"""
Showing how to use the gui (nice for debugging)
"""

import math

from pod import pods,world,gui       

# world definition file

worldFile="worlds/carCircuit.world"

# use a control object to do thrust steer etc.
control=pods.Control()

# create  the world
world=world.World(worldFile)  
pod=pods.CarPod(world)

# I set the frame rate so the animation is real time (you can make it faster/slower if you want) 
simple_gui=gui.SimpleGui(frames_per_sec=int(1/world.dt),world=world,pods=[pod])

while True:
    control.up=.1
    control.left=.015
    pod.step(control)
    
    # YOu can display debug text if you want.
    mess=str(pod.state)
    simple_gui.set_message(mess)

    # refresh the display.
    simple_gui.display()
    
    if pod.state.collide:    
        pod.reset()    # This is how to put the pod back at the start.
    
    if simple_gui.check_for_quit():   # Provide a way pout for the user
        break

    