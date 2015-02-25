import cart
import math

import guisimple
import math
        
        
#### MAIN CODE #########################

        
# create a cart +  inverted pendulum
cart=cart.Cart()

# set the initial angle 
cart.setAngle(math.pi+0.05)


dt=0.1     # Time step for control 

gui=guisimple.Gui(10)

#frameRate=10     # slow down to 10 steps per second.

#screen = gui.init_surface((800,200)," CART +IP demo" )

while not gui.check_for_quit():       #  loop until user hits escape
    
    force=0.0
    
    # step the car for a single GUI frame        
    cart.step(force,dt)
     
    gui.update(cart)
   