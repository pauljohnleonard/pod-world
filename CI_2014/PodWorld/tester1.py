# This program can be used to verify your code before submission
#
# your code should live in a subdirectory of punters  
#

name="eespjl"

from pod import simulation,pods,world,gui
import sys,os,imp,time

###  START OF PROGRAM
world = world.World("worlds/carCircuit.world")


punters_path="punters/"+name

#http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder

sys.path.append(punters_path)
fin=open(punters_path+"/plugin.py",'r')
punter_mod=imp.load_source(name,punters_path+"/",fin)
sys.path.remove(punters_path)   
default_dir=os.getcwd()
pod   = pods.CarPod(world)
  
    
# call the plugin to equip the car 
# set the current path to the punters directory
os.chdir(punters_path)
punter_mod.equip_car(pod)
os.chdir(default_dir)

controller=punter_mod.controller
 

simple_gui=gui.SimpleGui(frames_per_sec=int(1/world.dt),world=world,pods=[pod],back_ground=(5,5,5))

# use a control to activate the car.
control=pods.Control()

TIME_LIMIT=40.0
TRIPS_LIMIT=60.0

while True:

    
    controller(pod,control)    
    pod.step(control)
    
    simple_gui.set_message(str(pod.state))
          
    simple_gui.display()
    
    if pod.state.collide:
        dist=pod.state.pos_trips-pod.state.neg_trips+pod.state.seg_pos
        age=pod.state.age
        print " Crashed time=",age," progress =",dist
        score=dist
        break
       
    if pod.state.age > TIME_LIMIT:
        dist=pod.state.pos_trips-pod.state.neg_trips
        print " Time limit. Trips wires crossed =",dist
        score=dist
        break
    
    if pod.state.pos_trips - pod.state.neg_trips > TRIPS_LIMIT:
        print " Success you did it in ", pod.state.age, " secs "
        score=TRIPS_LIMIT + (TIME_LIMIT-pod.state.age)  
        break
    
    if simple_gui.check_for_quit():     #  We need to do this on some systems to avoid pygame hanging.
        print " User abort "
        score=0.0
        break
    
    
print " Your  score = ",score

    
    
         
        
