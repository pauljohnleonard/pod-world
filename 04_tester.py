#
# This program can be used to verify your code before submission
#
# your code should live in a subdirectory of punters matching your user name
# This code attempts to load plugin.py
#
#  For the module loading to work you need a file called __init__.py  in your plugin folder and the punters folder.
#
#  BY default this should run the plugin in eespjl.
#
import sys,importlib
import sys,os,imp,time,traceback


import scorer
from pod import simulation,pods,world,gui



GUI = True
FPS_FACT=20

if len(sys.argv) > 1:
    name=sys.argv[1]
else:
    name="eespjl"

if len(sys.argv) > 2:
    world_name=sys.argv[2]
else:
    world_name="pjl_chick"

###  START OF PROGRAM
track = world.World("worlds/"+world_name+".world")


punters_path="punters/"+name
default_dir=os.getcwd()


try:

    os.chdir(punters_path)
    pod   = pods.CarPod(track)
    plug=importlib.import_module('punters.'+name+'.plugin')
    plug.equip_car(pod)
    os.chdir(default_dir)
    pod.controller=plug.controller

except:

    print name
    print "Unexpected error:", sys.exc_info()
    traceback.print_tb(sys.exc_info()[2])
    pod.mess="Loading Error: "+str(sys.exc_info()[0])
    os.chdir(default_dir)
    sys.exit(0)


os.chdir(default_dir)

if GUI:
    simple_gui=gui.SimpleGui(frames_per_sec=int(FPS_FACT/track.dt),world=track,pods=[pod],back_ground=(5,5,5))

while True:

    pod.controller(pod)
    pod.step()

    if GUI:
        simple_gui.set_message(str(pod.state))
        simple_gui.display()
        if simple_gui.check_for_quit():
                sys.exit(0)

    score,kill,mess=scorer.evaluate(pod)
    if kill:
        print " mess=",mess
        print " score=",score
        break

    

    
    
         
        
