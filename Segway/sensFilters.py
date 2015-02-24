"""
Complementary Filter.  DO NOT MODIFY

Created by: Roberto La Spina

TO DO:
    -Work out what to do with encoderVal
    -Run-timer (timeit) on micropython compFilt and implement execution time in simulation? Artificially add in loop timer of students control system as an offset?

"""
import math

class CompFilter:
    """ 
    2-Wheeled inverted complementary filter.
    
    The robot's tilt angle 'phi' can be estimated from the acceleromter
    and gyroscope sensor readings
    
    The gyroscope suffers from drift over time whereas the accelerometer
    suffers from high noise and vibration
    
    The complementary filter combines the two to provide a reliable
    measure of the robots tilt, at the expense of some computational lag    
    """        
            
    def __init__(self, robot, timeConst = 0.075):
        """
        Initializes the instance of the complementary filter.

        :Parameters:
          robot
            Instance of the robot from which sensors are being read 
          timeConst
            Time constant of complementary filter (s)
        """    
            
        #New Paramters:
        self.timeConst = timeConst
        self.phiFilt = robot.getPhi()%(2*math.pi)

    def compFilter(self, dt_loop, robot, phiFilt = 20.0, timeConst = 0.):
        """
        Complementary filter used to accurately derive the robot's
        tilt angle from the IMU readings
        
        :Filter Paramters:    
          dt_loop
            Time elapsed since the last time the filter was called (s)
          robot
            Instance of the robot from which sensors are being read
          phiFilt
            Initial robot tilt angle when simulation is first started (degrees)
          gyroRate
            Gyroscope tilt angle velocity reading (degree/s)
          accelGZ
            Acceleromter output along Z (vertical) axis (g)
          accelGY
            Acceleromter output along Z (vertical) axis (g)
          encoderVal
            Encoder reading of wheel angle (TO BE EDITED)
        """
        #Check if an alternative time constant has been provided
        if (timeConst == 0.):
            timeConst = self.timeConst
        
        #Check if a valid tilt angle has been input to initialize the filter after a reset    
        if (phiFilt >= math.pi)^(phiFilt <= -math.pi):
            phiFilt = self.phiFilt
        
        #Calculate filter blending constant 'a'
        a=timeConst/(timeConst+dt_loop)
        
        #Calculate angle as measured by accelerometer
        [gyroRate, accelGZ, accelGY, encoderVal] = robot.readSensors()
        accelAng = -math.atan2(accelGY, accelGZ)
        
        #Combine gyro and accelerometer angle measurements using the complementary filter
        self.phiFilt = a*(phiFilt + gyroRate*dt_loop) + (1-a)*(accelAng)
    
        return self.phiFilt