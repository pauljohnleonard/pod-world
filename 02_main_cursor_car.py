from pod import pods,world,gui
import math
      
#### MAIN CODE #########################

# world definition file

worldFile="worlds/rectWorld.world"


# create  the world
world=world.World(worldFile)  


pod=pods.CarPod(world)

simple_gui=gui.SimpleGui(frames_per_sec=int(1.0/world.dt),world=world,pods=[pod])


while True:
    keys=simple_gui.get_pressed()
     
    #http://thepythongamebook.com/en:glossary:p:pygame:keycodes
    
    # The car has 4 controls that can have a value between 0-1
    
    #                             up- accelerate
    #                          down - brake
    #                          left - steer left
    #                          right - steer right
    #    
    if keys[gui.keys.K_UP]:
        pod.control.up=1.0
    else:
        pod.control.up=.0
          
    if keys[gui.keys.K_DOWN]:
        pod.control.down=1.0
    else:
        pod.control.down=.0


    if keys[gui.keys.K_LEFT]:
        pod.control.left=.2
    else:
        pod.control.left=.0
  
    if keys[gui.keys.K_RIGHT]:
        pod.control.right=.2
    else:
        pod.control.right=.0
      
        
    # Simulate dt of time
    pod.step()
    
    
    simple_gui.set_message(str(pod.state))  
    
    simple_gui.display()
    
    if pod.state.collide:
        pod.reset()
        
    if simple_gui.check_for_quit():
        break
    

    