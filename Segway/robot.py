"""
Inverted Pendulum model.  DO NOT MODIFY

Created by: Dr. Paul Leonard
Modified by: Roberto La Spina

TO DO:
    -Figure out what to do with encoder sensor reading
    -CHECK IF ACCELEROMTER IS POSITIVE UP OR DOWN and edit accelModel and CompFilter accordingly
    -Acceleromter cross-talk?
    -Add motor inductance effect? Include in RK scheme?
"""
import numpy
import rungekutta
import math
import random

class Robot:
    """ 
    2-Wheeled inverted pendulum model.
    
    The robot's motion is described according to two generalized coordinates: O and beta.
        O = angular displacement of the wheel from a starting position
        phi = angular tilt of the robot's body with respect to the vertical.
        beta = O - phi
         
    The state of the robot is described by the generalized coordinates and their first derivatives:
        state = [O, dO/dt, beta, dbeta/dt_dot]
     
    Given a configuration and the current state this allows the calculation of dstate/dt.
    
    This can then be used in a numerical integration to model the dynamics of the system.
    
    Angles are positive in a clockwise direction.
    
    Angle O is measured from the vertical starting at 12 o'clock.
    
    Angle beta is measured relative to angle O.
    
    X displacement increases from left to right as a function of wheel radius and angle O.
    
    """        
            
    def __init__(self,
                 L = 0.07,
                 Mb = 1.2,
                 Mw = 0.8,
                 Mm = 0.1,
                 Ib = 0.001,
                 Iw = 0.001,
                 Im = 0.0,
                 gN = 30,
                 wR = 0.085/2,
                 us = 0.000005,
                 ug = 0.0,
                 tau = 0.0,
                 g = 9.80665,
                 pwmRatio = 0.0,
                 Ke = 0.1680,
                 Kt = 0.3028,
                 Ra = 2.4,
                 Vdc = 3.7*3,
                 dt=0.001,
                 gyroPhi_dot = 0.0,
                 dt_gyro = 1.0/8000.0,  #8kHz gyroscope sampling
                 t_gyroOldPhi_dot = 0.0,
                 accelGZ = 0.0,
                 accelGY = 0.0,
                 dt_accel = 1.0/1000, #1kHz acceleromter sampling
                 t_accelOldG = 0.0,
                 encoderVal = 0.0,
                 dt_encoder = 0.05, #Count encoder interrupts every 500ms
                 dt_gui=0.05):
        """
        Initializes the 2-wheeled pendulum robot.

        :Parameters:
          L
            Length from wheel axle to center of gravity of the body (m)
          Mb
            Mass of the body at the centre of gravity of the body (kg)
          Mw
            Mass of the wheels with centre of gravity on the wheel axle (kg)
          Mm
            Mass of the motor's rotor shaft assumed in line with the wheel axle (kg)
          Ib
            Inertia of the body about the axis parallel to the wheel axle 
            and through the body's centre of gravity (kg*m^2)
          Iw
            Inertia of the wheels about the wheel axle (kg*m^2)
          Im
            Inertia of the motor's rotor shaft about the wheel axle (kg*m^2)
          gN
            Motor gearing ratio -> 30:1 for Pololu motors in use
          wR
            Wheel radius (m)
          us
            Kinetic coefficient of friction between motor rotor and housing
            as well as gearing (N*s) -> Ts = us*O_dot = friction torque
          ug
            Rolling resistance of wheel (N*s) -> Tg = ug*O_dot = rolling torque
          tau
            Input disturbance torque e.g. pushing the robot over (Nm)
          g
            Gravitational acceleration (m/s^2)
          pwmRatio
            Ratio of high-time to the total perdiod of the pwm waveform
          Ke
            Motor back-EMF constant
          Kt
            Motor torque constant
          Ra
            Motor armature winding resistance
          Vdc
            DC voltage supplied by onboard batteries. This value is randomized
            on each reset between the min and max allowed charge values of the
            batteries to reflect the changes in motor response due to battery
            discharge
          dt
            Time step for physical simulation (s)
          gyroPhi_dot
            Current gyroscope sensor reading of the robots angular tilt velocity
            including noise and quantization errors for the MPU9150 gyro (degrees/s)
          dt_gyro
            Gyroscope sampling rate setting (s)
          t_gyroOldPhi_dot
            Time of last gyroscope sample (s)
          accelGZ
            Current accelerometer sensor Z axis reading of the gravity component
            including noise and quantization errors for the MPU9150 accelerometer (g)
          accelGY
            Current accelerometer sensor Y axis reading of the gravity component
            including noise and quantization errors for the MPU9150 accelerometer (g)
          dt_accel
            Accelerometer sampling rate setting (s)  
          t_accelOldG
            Time of last accelerometer sample (s)
          dt_gui
            Time step for gui refreshing (display)
        """    
            
        #New Paramters:
        self.L = L
        self.Mb = Mb
        self.Mw = Mw
        self.Mm = Mm
        self.Ib = Ib
        self.Iw = Iw
        self.Im = Im
        self.gN = gN
        self.wR = wR
        self.us = us
        self.ug = ug
        self.tau = tau
        self.pwmRatio = pwmRatio
        self.Ke = Ke
        self.Kt = Kt
        self.Ra = Ra
        self.Vdc = Vdc
        self.g = g
        self.state = numpy.zeros(4) #[O, O_dot, beta, beta_dot]
        self.dt = dt
        self.gyroPhi_dot = gyroPhi_dot
        self.dt_gyro = dt_gyro
        self.t_gyroOldPhi_dot = t_gyroOldPhi_dot
        self.accelGZ = accelGZ
        self.accelGY = accelGY
        self.dt_accel = dt_accel
        self.t_accelOldG = t_accelOldG
        self.encoderVal = encoderVal
        self.dt_encoder = dt_encoder
        self.dt_gui=dt_gui
        self.time = 0.0             #Initialize simulation time
        self.rk=rungekutta.RungeKutta(self.state,0,dt,self)

    def _eval(self,time,state,state_dot):
        """
        Given the state vector
        Set the state vector, calculate state_dot using the dynamical equations.
        Used by numerical integration. Do not use this directly.
        """               
        L = self.L
        Mb = self.Mb
        Mw = self.Mw
        Mm = self.Mm
        Ib = self.Ib
        Iw = self.Iw
        Im = self.Im
        gN = self.gN
        wR = self.wR
        us = self.us
        ug = self.ug
        tau = self.tau
        pwmRatio = self.pwmRatio
        Ke = self.Ke
        Kt = self.Kt
        Ra = self.Ra
        Vdc = self.Vdc
        g = self.g
        time = self.time
        dt_gyro = self.dt_gyro
        t_gyroOldPhi_dot = self.t_gyroOldPhi_dot
        dt_accel = self.dt_accel
        t_accelOldG = self.t_accelOldG
        
        Mr = Mw + Mm
        
        O=state[0]
        O_dot=state[1]
        beta=state[2]
        beta_dot=state[3]      
   
        #"""
        #PWM Motor Control
        
        #Calculate voltage across armature as function of PWM input ratio
        Va = abs(pwmRatio) * Vdc
        
        #Calculate motor output torque
        Tq = (((Kt*Va) - (Kt*Ke*O_dot))/Ra)*math.copysign(1,pwmRatio)
        #"""
        
        """
        #Direct Torque Control - for debugging PWM motor control and not for standard usage
        
        Tq = pwmRatio       
   
        """
        #Idealized Robot Dynamics (no moments of inertia or friction losses)
        
        a1 = (-Mb*(L**2)) - (Mb*L*wR*math.cos(O-beta))
        a2 = Mb*(L**2)
        a3 = Mb*g*L*math.sin(O-beta)
        
        b1 = ((Mb+Mr)*(wR**2)) + (Mb*(L**2)) + (2*Mb*L*wR*math.cos(O-beta))
        b2 = (-Mb*(L**2)) - (Mb*L*wR*math.cos(O-beta))
        b3 = (-Mb*L*wR*O_dot*(O_dot-beta_dot)*math.sin(O-beta)) + (Mb*L*wR*beta_dot*(O_dot-beta_dot)*math.sin(O-beta)) - (Mb*g*L*math.sin(O-beta))
        
        beta_dot_dot = ((b1*(Tq+tau)) - (a3*b1) + (a1*b3)) / ((a2*b1) - (a1*b2))
        O_dot_dot = (-b3 - (b2*beta_dot_dot)) / b1
        #"""
        
        #"""
        #Real Robot Dynamics
        
        a1 = (-Mb*(L**2)) - (Mb*L*wR*math.cos(O-beta)) - Ib
        a2 = (Mb*(L**2)) + Ib + Im*(gN**2)
        a3 = (Mb*g*L*math.sin(O-beta)) + (us*beta_dot)
        
        b1 = (Mb*(wR**2)) + (Mb*(L**2)) + (2*Mb*L*wR*math.cos(O-beta)) + (Mr*(wR**2)) + Iw + Ib
        b2 = -Mb*(L**2) - Mb*L*wR*math.cos(O-beta) - Ib
        b3 = (ug*O_dot) - Mb*((L*wR*((O_dot-beta_dot)**2)*math.sin(O-beta)) + (g*L*math.sin(O-beta)))
        
        beta_dot_dot = ((b1*(Tq+tau)) - (a3*b1) + (a1*b3)) / ((a2*b1) - (a1*b2))
        O_dot_dot = (-b3 - (b2*beta_dot_dot)) / b1
        #"""
        
        """
        print "O: ",O
        print "O_dot: ",O_dot
        print "O_dot_dot: ",O_dot_dot
        print "beta: ",beta
        print "beta_dot: ",beta_dot
        print "beta_dot_dot: ",beta_dot_dot
        print " "
        #"""
        
        #Update state_dot vector with robot dynamics output       
        state_dot[0]=state[1]
        state_dot[1]=O_dot_dot
        state_dot[2]=state[3]
        state_dot[3]=beta_dot_dot
        
        #Update current sensor sample values
        if (time-t_gyroOldPhi_dot) >= dt_gyro:
            self.gyroPhi_dot = self.gyroModel()
            self.t_gyroOldPhi_dot += int((time-t_gyroOldPhi_dot) / dt_gyro) * dt_gyro
            
        if (time-t_accelOldG) >= dt_accel:
            [self.accelGZ, self.accelGY] = self.accelModel()
            self.t_accelOldG += int((time-t_accelOldG) / dt_accel) * dt_accel        

    def getX(self):
        """
        Return the horizontal displacement of the Robot
        """
        x_dist = self.state[0] * self.wR

        return x_dist
    
    def getO(self):
        """
        Returns the angle of the wheels
        """
        return self.state[0]
    
    def getBeta(self):
        """
        Returns the angle of the pendulum with respect to the wheel angle
        """
        return self.state[2]
    
    def getPhi(self):
        """
        Returns the angle of the pendulum with respect to the vertical
        """
        phi = self.state[0]-self.state[2]
        
        return phi
    
    def getPhi_dot(self):
        """
        Returns the angular tilt velocity of the pendulum
        """
        phi = self.state[1]-self.state[3]
        
        return phi
    
    def getState(self):
        """
        Returns the whole state vector  [O, dO/dt, beta, dbeta/dt]
        """
        return self.state
        
    def setInputs(self, pwmRatio, torque):
        '''
        Sets the torque applied to the Robot.
        '''
        self.pwmRatio=pwmRatio
        self.tau=torque
        
    def reset(self, O = 0., O_dot = 0., beta = 0., beta_dot = 0.):
        """
        Resets the state of the pendulum and the simulation timer

        :Parameters:
          O
            Angular position of the wheel, clockwise from the vertical (rad)
          O_dot
            Angular velocity of the wheels (rad/s)
          beta
            Angular tilt of the robot's body, clockwise from O (rad)
          beta_dot
            Angular tilt velocity of the robot (rad/s)
            
        """
        #New state:
        self.state[0] = O
        self.state[1] = O_dot
        self.state[2] = beta
        self.state[3] = beta_dot
        
        #Reset simulation timers
        self.time=0.0 
        self.t_accelOldG=0.0
        self.t_gyroOldPhi_dot=0.0      
        self.rk.time=0.0
        
        #Randomize battery voltage
        self.Vdc = random.uniform(2.75,4.2)*3
        
    def setAngle(self, body_phi = 0., wheel_O = 0., body_phi_dot = 0., wheel_O_dot = 0.):
        """
        Resets the angles to desired values
        """
        body_beta = wheel_O - body_phi
        body_beta_dot = wheel_O_dot - body_phi_dot
        
        self.reset(wheel_O, wheel_O_dot, body_beta, body_beta_dot)        
        
    def step(self,pwmRatio,torque,dt_gui):
        """      
        Advances the physical model by dt_gui.
        Uses the runge-kutta numerical integration scheme.
        
        torque
            Input disturbance torque i.e. pushing the robot over
        """
    
        self.setInputs(pwmRatio, torque)
        self.rk.step(dt_gui)
        
    def readSensors(self):
        """
        Returns current gyroscope, acceleromter and wheel encoder readings
        """
        return [self.gyroPhi_dot, self.accelGZ, self.accelGY, self.encoderVal]
    
    def gyroModel(self):
        """
        Model of the gyro sensor on the MPU9150 IMU board
        Produces a realistic gyroscope output accounting for noise and quantization
        
        :Sensor Paramters:
            gyroRMS
                Gyro RMS Noise (degrees/s - rms)
            gyroSens
                Gyro sensitivity (LSB /degrees/S)
            gyroRes
                Gyroscope resolution (degrees/S)
        """   
        gyroRMS = 0.06
        gyroSens = 65.5
        gyroRes = 1.0/gyroSens

        #Add noise to gyro reading according to datasheet specs
        phi_dot = self.getPhi_dot()
        noisy_phi_dot = random.normalvariate(phi_dot, gyroRMS)
        
        #Quantize gyro reading according to datasheet specs             
        noisy_phi_dot = int(noisy_phi_dot / gyroRes) * gyroRes 
        
        return noisy_phi_dot
    
    def accelModel(self):
        """
        Model of the accelerometer sensor on the MPU9150 IMU board
        Produces a realistic accelerometer output accounting for noise and quantization
        Accelerometer is assumed to be located on wheel axle. Hence no other forces,
        except gravitational acceleration, are measured when robot rotates.
        
        :Sensor Paramters:
            accelRMS
                Accelerometer RMS Noise (g - rms)
            accelSens
                Gyro sensitivity (LSB/g)
            accelRes
                Gyroscope resolution (g)
        """   
        accelRMS = 0.004
        accelSens = 16384
        accelRes = 1.0/accelSens
        
        #Add noise to accel reading according to datasheet specs
        phi = self.getPhi()
        accelGZ = math.cos(phi)    #Acceleromter output in 'g' along Z (vertical) axis
        accelGY = -math.sin(phi)    #Acceleromter output in 'g' along Y (horizontal) axis
        noisy_accelGZ = random.normalvariate(accelGZ, accelRMS)
        noisy_accelGY = random.normalvariate(accelGY, accelRMS)
        
        #Quantize accel reading according to datasheet specs             
        noisy_accelGZ = int(noisy_accelGZ / accelRes) * accelRes
        noisy_accelGY = int(noisy_accelGY / accelRes) * accelRes 
        
        return [noisy_accelGZ, noisy_accelGY]
        
