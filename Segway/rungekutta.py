
"""
DO NOT MODIFY
Time steps a system using runge-kutta 4th order numerical integration
Uses a time step of h
"""
import numpy

class RungeKutta:

    def __init__(self, state,time, h,model):
        """
        Initialise simulation 
        state -- starting state
        time -- time
        h -- runga kutta time step
        model -- physical model  
        """
        self.n = len(state)
    
        self.time=time;
        self.h=h;
        self.model=model;
        self.state=state;
        self.init()

    def init(self):
            
        self.state_dot1 = numpy.zeros(self.n)
        self.state_dot2 = numpy.zeros(self.n)
        self.state_dot3 = numpy.zeros(self.n)
        self.state_dot4 = numpy.zeros(self.n)
        self.state1 = numpy.zeros(self.n)
        self.state2 = numpy.zeros(self.n)
        self.state3 = numpy.zeros(self.n)
        
    def stepRK(self):
        """
        Perform one runga kutta time step
        """

        # 1. initial state_dotocity at time
        tstart = self.time
        self.model._eval(tstart, self.state, self.state_dot1)

        # 2. state_dotocity at time+h/2 using previous state_dot estimate
        tmid = self.time + self.h/ 2.0

        for i in xrange(self.n):
            self.state1[i] = self.state[i] + self.h * self.state_dot1[i] * 0.5
        

        self.model._eval(tmid, self.state1, self.state_dot2)

        # 3. redo using new state_dotocity estimate
        for i in xrange(self.n):
            self.state2[i] = self.state[i] + self.h * self.state_dot2[i] * 0.5
      
        self.model._eval(tmid, self.state1, self.state_dot3)

        # 4. estimate state_dotocity at end
        tend = self.time + self.h;
        for i in xrange(self.n):
            self.state3[i] = self.state[i] + self.h * self.state_dot3[i] * 0.5
      
        self.model._eval(tend, self.state3, self.state_dot4)
        
        for i in xrange(self.n):
            self.state[i] += self.h * (self.state_dot1[i] + 2.0 * self.state_dot2[i] + 2.0 * self.state_dot3[i] + self.state_dot4[i])/ 6.0

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
    