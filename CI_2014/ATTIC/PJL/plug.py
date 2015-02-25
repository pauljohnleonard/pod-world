
import math

INIT_ANG=0.3
TRUN=500.0
GOAL=TRUN-0.01
X_MAX=5.0

def reap(cart):
    
    if cart.time > TRUN:
        return   TRUN - abs(cart.getX());
    
    if (abs(math.pi-cart.getAngle()) > INIT_ANG) or (abs(cart.getX()) > X_MAX):
        return cart.time
    
    return None 


