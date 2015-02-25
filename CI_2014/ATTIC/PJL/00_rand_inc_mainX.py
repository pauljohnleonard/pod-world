
import cart
import math
import gui
import random
import brain
import copy



def randomSeed():
    """
    Random number between -0.5  and 0.5
    """
    return (0.5 - random.random())


def randomWeights(sizes,fact): 
            weight=[]
            
            for i in range(len(sizes)-1):  
                layer=[]
                for _ in range(sizes[i+1]):
                    w=[]
                    for _ in range(sizes[i]):
                        w.append(randomSeed()*fact)
                    w.append(randomSeed()*fact)
                    layer.append(w)
                weight.append(layer)
                
            return weight
                

# example showing how you might mutate the weights
def mutate(weights_orig,mutate_amount):
    # copy original into a new array
    w=copy.deepcopy(weights_orig)

    for layer in xrange(len(w)):
        for neuron in xrange(len(w[layer])):
            for i in xrange(len(w[layer][neuron])):
                w[layer][neuron][i] += randomSeed()*mutate_amount 
     
    return w

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

# set the initial angle 
cart.setAngle(math.pi+0.02)



frameRate=10     # slow down to 10 steps per second.

screen = gui.init_surface((800,200)," CART + IP demo" )

first=True
graphics=False
best_fit=-1e32
tot_time=0.0
best_guess=None
inc=False
force_scale=10.0

sizes=[4,1]
net=None

INIT_ANG=0.3

cnt=0
GOAL=500.0
TOTAL_TIME_MAX=10000

while not gui.check_for_quit():       #  loop until user hits escape
  
    # Test for falling over
    # if fallen then reset with a random angle 
    
    if first or abs(math.pi-cart.getAngle()) > INIT_ANG:
        if not first:
            
           state=cart.getState()
           fit=time - cart.getX()
           print cnt,best_fit,fit,tot_time,state,net.weight
           if fit > best_fit:
               cnt=0
               best_fit=fit
               best_guess=copy.deepcopy(guess)
 
           
           
        cart.setAngle(math.pi+INIT_ANG)
        cnt += 1
        
        if not inc or best_guess == None or (cnt % 10 == 0):
            guess=randomWeights(sizes,1.0)
            #cnt=0
        else:
            scale=random.random()*0.001
            guess=mutate(best_guess,scale)
            

        if net == None:      
            net=brain.FeedForwardBrain(weight=guess)
        else:
            net.setWeights(guess)
       
        time=0;  
        first=False
  
    input = copy.deepcopy(cart.getState())
    input[0]=input[0]-math.pi
    out=net.ffwd(input)
    
    force=(out[0]-0.5)*force_scale
 
    # step the car for a single GUI frame        
    cart.step(force,dt)
    
    time+=dt
    tot_time+=dt
    
    fit=time-cart.getX()
    if fit > GOAL or tot_time > TOTAL_TIME_MAX:
        brain.saveBrain(net)
        break
        
    ################  RESET CODE ##############################
    
  
        
    ############################################################
    
    if graphics:
        # draw the cart and display info
        draw(screen,cart,force)
    
        # slow the gui down to the given frameRate
        gui.tick(frameRate)
        
if time > GOAL:
    print " SUCCESS ",time,tot_time
    
else:
    print " best =",best_fit