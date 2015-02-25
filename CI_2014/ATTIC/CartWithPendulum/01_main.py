import cart
import math

# create an inverted pendulum
cart=cart.Cart()

PI=math.pi

# reset and set the initial angle just off verticle 
cart.setAngle(PI-0.1)

force=0    # Force applied to cart


dt=0.1     # Time step for control 

while True:
    
    
    cart.step(force,dt)
    state=cart.getState()
    print "phi= ",state[0], "  dphi/dt=",state[1]," x=",state[2]," dx/dt=",state[3]
    
    #  If we fall over exit
    if state[0] < PI*0.5  or state[0] > PI*1.5:
        break