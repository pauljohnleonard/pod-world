
# This code would be a good place to start your evolution coding.

import math
from pod import world,gui,pods       
  
# flag to switch GUI on/off  
GUI=True

def equip_car(pod):
          
    sensors=[pods.Sensor(angle=0.4,name="Left"),pods.Sensor(angle=-0.4,name="Right")]
    pod.addSensors(sensors) 
    pod.col=(0,255,0)
    
    pod.my_data="Cool festure of python. YOu can add your own data to an object"

def controller(pod,control):
    """
    In your system you would be wanting to change parameters that are used here after each evaluation.
    """
    state=pod.state
    sensors=pod.sensors
    
    vel=state.vel
    
    if vel < 100:
        control.up=0.5
    else:
        control.up=0.0
       
       
    left=sensors[0].val
    right=sensors[1].val
    print left,right
    
    if left < right:
        control.left=0
        control.right=.5
  
    else:
        control.left=.5
        control.right=0

def evaluate(pod):
    """
    Showing how you can evaluate the performance of your car.
    """
    
    # reset the state of the car before starting
    pod.reset()
    
    while True:
    
        if GUI:
            mess=str(pod.state)
            simple_gui.set_message(mess)
            simple_gui.display()
            
            if simple_gui.check_for_quit():
                break
    
        if pod.state.collide:
            return pod.state.pos_trips-pod.state.neg_trips+pod.state.seg_pos  
        
        if pod.state.pos_trips-pod.state.neg_trips > 15:
            return 100
        
        controller(pod,control)      
        pod.step(control)
        

worldFile="worlds/carCircuit.world"


# use a control to activate the car.
control=pods.Control()

# create  the world
world=world.World(worldFile)  
dt=world.dt

pod=pods.CarPod(world)
equip_car(pod)


if GUI:
     #frames_per_sec=int(1/dt)
 
    frames_per_sec=4
    simple_gui=gui.SimpleGui(frames_per_sec=frames_per_sec,world=world,pods=[pod])

print " Performance=",evaluate(pod)
