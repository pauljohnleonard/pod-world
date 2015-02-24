import random
import math

class Controller:
    
    def __init__(self):
        self.e_new = 0
        self.e_old = 0
        self.e_int = 0
        self.e_diff = 0
        self.P = 5
        self.I = 0.1
        self.D = 0.2
        self.Tq = 0

    def PD(self, O, O_dot, phi, phi_dot):
    
        e_new = self.e_new
        e_old = self.e_old
        e_int = self.e_int
        e_diff = self.e_diff
        P = self.P
        I = self.I
        D = self.D
        Tq = self.Tq
        
        e_old = e_new
        e_new = phi
        e_int = e_old + e_new
        e_diff = phi_dot
        
        Tq = P*e_new + I*e_int + D*e_diff
        
        #Limit controller output to motor stall torque
        if Tq > 1:
            Tq = 1
        elif Tq < -1:
            Tq = -1
        
        #print Tq
    
        return Tq
    