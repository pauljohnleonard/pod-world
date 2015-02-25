import gui
import math

class Gui:
    
    
    def __init__(self,framerate=10):
        
        """
            framerate (frames per second) defines the maximum refresh rate.
            update will wait to maintain this rate
        
        """

        self.frameRate=10     # slow down to 10 steps per second.

        self.screen = gui.init_surface((800,200)," CART +IP demo" )

        self.frameRate=framerate
        
        
    
    def update(self,cart):
        """
        update the gui drawing the cart.
        wait if to maintain the required framerate.
        """
        
        self._draw(cart)
   
        gui.tick(self.frameRate)  
        
    def check_for_quit(self):
        """
        See if the user has closed the window.
        """
        return gui.check_for_quit() 
      
      
    def _draw(self,cart):
        """
        Called by the simulation to display the current state of the cart.
        """ 
        
        screen=self.screen
        
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
        str2+= " force: %5.2f " % cart.F
        
        gui.draw_string(screen,str2,(20,10),col,16)
        
        # copy screen onto the display 
        gui.blit(screen)
   