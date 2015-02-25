"""
Inverted Pendulum model.  DO NOT MODIFY
"""

import numpy
import rungakutta
import math

class Cart:
    """ 
    Cart and Inverted pendulum model.
     
    Given a configuration and the current state this will allow you to calculate the dstate/dt.
    
    This can then be used in a numerical time stepping to model the dynamics of the system.
    
    All angles are in radians   range is 0 - 2pi.
    
    At it's lowest point the angle is 0
    
    When the pendulum is vertical the angle is PI   (this avoids wrap around during normal operation)
    
    phi increases in the anti clockwise direction
    
    X increases from left to right.
    
    """        
            
    def __init__(self,dt_gui=0.05, length = 1.5, mass = 1., mass_cart = .1,dt=0.001):
        '''
        Initializes the pendulum.

        :Parameters:
          length
            Pendulum length (in meters)
          mass
            Pendulum mass (in kilograms)
          mass_cart
            Cart mass (in kilograms)
          dt
            Time delta for physical simulation (in seconds)
          dt_gui
            Time step for each gui step (display)
        '''
        self.dt_gui=dt_gui
        self.l = length
        self.m = mass
        self.mc = mass_cart
        self.dt = dt
        self.state = numpy.zeros(4)
        self.time=0.0
        self.rk=rungakutta.RungeKutta(self.state,0,0.01,self)


    def reset(self, O = 0., w = 0., x = 0., v = 0.):
        '''
        Sets the state of the pendulum.

        :Parameters:
          O
            Angular position in radians (theta)
          w
            Angular velocity in radians/second (omega)
          x
            Position of the cart in meters
          v
            Speed of the cart     in meters/second
        '''
        self.state[0] = O
        self.state[1] = w
        self.state[2] = x
        self.state[3] = v
        self.time=0.0
        self.rk.time=0.0
        
    def _eval(self,time,state,vel):
        """
        Given the state vector
        Set the velocity vector vel using the dynamical equations.
        Used by time step schemes. Do not use this directly.
        """
        
        g = 9.80665       # Gravity in m/s^2
        l = self.l
        
        O=state[0]
        w=state[1]
        #x=state[2]
        #vel=state[3]
        
        so = math.sin(O)
        co = math.cos(O)
        m2 = self.m
        m1 = self.mc
        phi=O
        Fphi=0
        Fx=self.F
        n = 2*l*m2*math.cos(phi)*Fx + 2*(m1+m2)*(-Fphi + g*l*m1*math.sin(phi)) + l*m2*m2*math.sin(2*phi)*w*w;
        
        d = l*l*m2*(-2*m1-m2+m2*math.cos(2*phi));
        
        q= n/d;  #// w'
        
# linear accel        
       # a = F - (m*l*(w*w*so - q*co)) / M
        
        n = 2*(l*Fx - math.cos(phi) * Fphi + l * math.sin(phi)* ( g * m1 * math.cos(phi) + l * m2 * w * w));
        
        d  = l * (2*m1 + m2 - m2 * math.cos(2*phi));
        
        a=n/d;  #// v'
        
        vel[0]=state[1]
        vel[1]=q
        vel[2]=state[3]
        vel[3]=a

    def getX(self):
        """
        return the position of the cart
        """
        return self.state[2]
    
    def getAngle(self):
        """
        returns angle of pendulum
        """
        return self.state[0]
    
    def getState(self):
        """
        return the whole state vector  [ X DX/DT  PHI DPHI/DT ]
        """
        return self.state
        
    def setForce(self, F ):
        '''
        set the force applied to the cart.
        '''
        self.F=F
        
        
    def setAngle(self,ang):
        """
        reset everything and set initial angle [rads]  (0 is down) 
        """
        self.reset(ang)
        
        
    def step(self,force,dt):
        """      
        Advances the physical model by dt.
        Uses the runga-kutta scheme 
        """
    
        self.setForce(force)
        self.rk.step(dt)
        
