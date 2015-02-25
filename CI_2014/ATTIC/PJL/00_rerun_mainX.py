import cart
import math
import gui
import random
import brain
import copy



def draw(screen,cart,force):
        """
        Called by the simulation to display the current state of the cart.
        """ 
        
        # clear screen
        screen.fill((0,0,0))
 
        # get the size of the window
        wid=gui.dim_window[0]
        hei=gui.dim_window[1]
        
        # pendulum length
        length=cart.l
        scale=hei/length/3.0
        
        # map position onto the screen 
        x1=wid/2.0+cart.getX()*scale
        
        # if too big/small limit the position
        if x1 > wid*.8:
            x1 =wid*.8
        if x1 < wid*.2:
            x1 = wid*.2
        
        # base line for the cart    
        y1=hei*.6

        # angle of pendulum
        ang=cart.getAngle()
        
        # x,y of the end of pendulum
        x2=x1+scale*math.sin(ang)*length
        y2=y1+scale*math.cos(ang)*length
        
        # draw pendulum
        col=(255,0,0)
        thick=3
        gui.draw_line(screen,x1,y1,x2,y2,col,thick)
        col=(0,255,0)
        gui.fill_circle(screen,x2,y2,12,col)
        
        # draw cart
        col=(0,0,255)
        thick=20
        gui.draw_line(screen,x1-20,y1,x1+20,y1,col,thick)
        
        # display the state of the cart
        col=(0,255,255)
        
        state=cart.state
        str2=""
        str2+= "Phi: %5.2f "  % (state[0]-math.pi)
        str2+= "dphidt: %5.2f " % state[1]
        str2+= "x: %5.2f " % state[2]
        str2+= "dxdt: %5.2f " %state[3]
        str2+= " force: %5.2f " % force
        
        gui.draw_string(screen,str2,(20,10),col,16)
        
        # copy screen onto the display 
        gui.blit(screen)
        
        
#### MAIN CODE #########################


        
# create an inverted pendulum
cart=cart.Cart(dt=.01)

dt=.1



frameRate=10     # slow down to 10 steps per second.

screen = gui.init_surface((800,200)," CART + IP demo" )

force_scale=10.0



net=brain.loadBrain()

INIT_ANG=0.3

cart.setAngle(math.pi)
cart.state[2]=-1.0


while not gui.check_for_quit():       #  loop until user hits escape
  
    # Test for falling over
    # if fallen then reset with a random angle 
      
    input = copy.deepcopy(cart.getState())
    input[0]=input[0]-math.pi
    out=net.ffwd(input)
    
    force=(out[0]-0.5)*force_scale
 
    # step the car for a single GUI frame        
    cart.step(force,dt)
    
        # draw the cart and display info
    draw(screen,cart,force)
    
        # slow the gui down to the given frameRate
    gui.tick(frameRate)

