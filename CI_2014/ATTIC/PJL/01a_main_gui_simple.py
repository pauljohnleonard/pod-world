import cart
import math

import guisimple
import math
import brain
import random
import copy




 
        
#### MAIN CODE #########################

        
# create a cart +  inverted pendulum
cart=cart.Cart()

# set the initial angle 
cart.setAngle(math.pi+0.05)



dt=0.1     # Time step for control 

gui=guisimple.Gui(10)


  
while not gui.check_for_quit():       #  loop until user hits escape
    

  
    
    # step the car for a single GUI frame        
    cart.step(force,dt)
     
    gui.update(cart)
   