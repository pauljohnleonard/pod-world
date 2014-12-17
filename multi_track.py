"""
Showing how to use the gui (nice for debugging)
"""

import math

from pod import pods,world,gui       

GUI=True

def test_world(pod,track):
    
    # the following will also reset the pod
    pod.setWorld(track)
    
    if GUI:
        simple_gui.setWorld(track)
    
    while True:
        control.up=.1
        control.left=.015
        pod.step(control)
        
        if GUI:       
            # refresh the display.
            simple_gui.display()
            
        if pod.state.collide:    
            return
        
        if GUI:
            if simple_gui.check_for_quit():   # Provide a way out for the user
                break

# world definition file

worldFiles=["worlds/carCircuit.world","worlds/pjl_chick.world"]

# use a control object to do thrust steer etc.
control=pods.Control()

# create  the world
worlds=[]

for worldFile in worldFiles:
    worlds.append(world.World(worldFile))
  

# You can now create a pod without a world by passing None
pod=pods.CarPod(None)

if GUI:
    # Note world.DEFAULT_DT is the standard time step 
    simple_gui=gui.SimpleGui(frames_per_sec=int(1/world.DEFAULT_DT),world=None,pods=[pod])
        
        
for w in worlds:
    test_world(pod,w)
    
    
    