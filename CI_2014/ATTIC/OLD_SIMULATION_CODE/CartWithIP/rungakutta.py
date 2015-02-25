
"""
DO NOT MODIFY

Time steps a system using runga-kutta 4th order 

Uses a time step of h
"""

import numpy

class RungeKutta:

    def __init__(self, state,time, h,model ):
        """
        Initialise simulation 
        state -- starting state
        time -- time
        h-- runga kutta time step
        model -- physical model  
        """
        self.n = len(state)
    
        self.time=time;
        self.h=h;
        self.model=model;
        self.state=state;
        self.init()

    def init(self):
            
        self.vel1 = numpy.zeros(self.n)
        self.vel2 = numpy.zeros(self.n)
        self.vel3 = numpy.zeros(self.n)
        self.vel4 = numpy.zeros(self.n)
        self.state1 = numpy.zeros(self.n)
        self.state2 = numpy.zeros(self.n)
        self.state3 = numpy.zeros(self.n)
        
        
    def stepRK(self):
        """
        Perform one runga kutta time step
        """

        # 1. initial velocity at time
        tstart = self.time
        self.model.eval(tstart, self.state, self.vel1)

        # 2. velocity at time+h/2 using previous vel estimate
        tmid = self.time + self.h/ 2.0

        for i in xrange(self.n):
            self.state1[i] = self.state[i] + self.h * self.vel1[i] * 0.5
        

        self.model.eval(tmid, self.state1, self.vel2)

        # 3. redo using new velocity estimate
        for i in xrange(self.n):
            self.state2[i] = self.state[i] + self.h * self.vel2[i] * 0.5
      
        self.model.eval(tmid, self.state1, self.vel3)

        # 4. estimate velocity at end
        tend = self.time + self.h;
        for i in xrange(self.n):
            self.state3[i] = self.state[i] + self.h * self.vel3[i] * 0.5
      
        self.model.eval(tend, self.state3, self.vel4)
        
        for i in xrange(self.n):
            self.state[i] += self.h * (self.vel1[i] + 2.0 * self.vel2[i] + 2.0 * self.vel3[i] + self.vel4[i])/ 6.0

        self.time +=self.h
        
    def reset(self):
        """
        Reset the model
        """
        
        self.time=0.0
        self.model.reset()
        self.init()
        
    def step(self,dt):
        """
        Perform runga-kutta time steps to advance the model by dt
        """
        
        tend=self.time+dt
        
        while(self.time < tend):
            self.stepRK()
            
            
        self.model.time=self.time
    