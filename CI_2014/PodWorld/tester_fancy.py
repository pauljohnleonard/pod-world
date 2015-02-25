# This program can be used to verify your code before submission
#
# your code should live in a subdirectory of punters  
#

name="me"

from pod import simulation,pods,world,gui
import sys,os,imp,time


# See 
#http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder


###  START OF PROGRAM


world = world.World("worlds/carCircuit.world")

punters_path="punters/"+name
sys.path.append(punters_path)
fin=open(punters_path+"/plugin.py",'r')
punter_mod=imp.load_source(name,punters_path+"/",fin)
sys.path.remove(punters_path)   
default_dir=os.getcwd()
pod   = pods.CarPod(world)
  
    
# call the pluginto equip the car 
# set the current path to the punters directory
os.chdir(punters_path)
punter_mod.equip_car(pod)
os.chdir(default_dir)

controller=punter_mod.controller
 

simple_gui=gui.SimpleGui(frames_per_sec=int(1/world.dt),world=world,pods=[pod],back_ground=(255,255,255))

# use a control to activate the car.
control=pods.Control()

pause=False

while True:

    if not pause:
        controller(pod,control)    
        pod.step(control)
    
        simple_gui.set_message(str(pod.state))
          
    simple_gui.display()
    
    if pod.state.collide:
        print "Crashed"
        break
    
    if simple_gui.check_for_quit():
        break
    
    if simple_gui.get_pressed()[gui.keys.K_p]:
        pause=True
        
        
    if simple_gui.get_pressed()[gui.keys.K_s]:
        pause=False
          
        
        
