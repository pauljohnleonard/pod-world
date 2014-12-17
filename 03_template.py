
# This code would be a good place to start your evolution coding.

import math,random
from pod import world,gui,pods       
  
# flag to switch GUI on/off  
GUI=True

def equip_car(pod):
          
    sensors=[pods.Sensor(angle=0.4,name="Left"),pods.Sensor(angle=-0.4,name="Right")]
    pod.addSensors(sensors) 
    pod.col=(0,255,0)
    pod.data=[100,2]    # default control system parameters
    
    

def controller(pod):
    """
    In your system you would be wanting to change parameters that are used here after each evaluation.
    """
    state=pod.state
    sensors=pod.sensors
    
    vel=state.vel
    
    if vel < pod.data[0]:
        pod.control.up=pod.data[1]
    else:
        pod.control.up=0.0
       
       
    left=sensors[0].val
    right=sensors[1].val
    
    print left,right
    
    if left < right:
        pod.control.left=0
        pod.control.right=.5
  
    else:
        pod.control.left=.5
        pod.control.right=0

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
        
        controller(pod)
        pod.step()
        

worldFile="worlds/carCircuit.world"



# create  the world
world=world.World(worldFile)  
dt=world.dt

pod=pods.CarPod(world)
equip_car(pod)


if GUI:
     #frames_per_sec=int(1/dt)
 
    frames_per_sec=4
    simple_gui=gui.SimpleGui(frames_per_sec=frames_per_sec,world=world,pods=[pod])


max_val=0     #    max_val keeps track of the best so far

def make_a_guess():
    return [3000*random.random(),random.random()]


searching=True
goal=100

while max_val < 100:
    
    pod.data=make_a_guess()
    
    fitness=evaluate(pod)
    
    if fitness > max_val:
        max_val=fitness
        max_data=pod.data
        print " best so far ",max_val,max_data
