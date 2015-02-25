'''
Created on 21 Dec 2010

@author: pjl
'''

NUMPY=False

if NUMPY:
    import numpy
    
import math
import util
import gui
import pygame
from pygame.locals import *
import os

ang_thrust_max=0.5
white = (255,255,255)
red=(255,40,40)
small=1e-6


    
class Control:
    " A control message "
    def __init__(self):
        self.left=0
        self.right=0
        self.up=0
        self.down=0

    def limit(self):
        " limit all values to 0-1 range "
        self.up=util.limit(self.up,0,1)
        self.right=util.limit(self.right,0,1)
        self.down=util.limit(self.down,0,1)
        self.left=util.limit(self.left,0,1)

class Sensor:
    """  
        ang_ref:  anticlockwise angle from forward 
        range: 
        name:
    """
           
    def __init__(self,ang_ref,range,name):
       
        
        self.ang_ref=ang_ref
        self.ang=ang_ref
        self.range=range
        self.val=0
        # self.val=0
        self.wall="None"
        self.name=name

    def to_string(self):
        return str(int(self.val*self.range))


class State: 
    def __repr__(self):
        txt=""
        for attr, value in self.__dict__.iteritems():
            txt+=str(attr)+ " "+ str(value)+"\n" 
     
        return txt
        
class Pod:
    """ Base class for all pods """
    
    pod_poly_ref=[(-10,-10),(0,20),(10,-10)]
    thrust_poly_ref=[(0,-10),(-2,-14),(0,-18),(2,-14)]
    left_poly_ref=[(-5,5),(-9,4),(-12,5),(-9,6)]
    right_poly_ref=[(5,5),(9,4),(12,5),(9,6)]
    brake_poly_ref=[(0,-16),(-5,-10),(0,-12),(5,-10)]
    

    def __init__(self,col):
       
        self.message="init"
        self.control=Control()
        self.sensors=[]
        self.base_init()    
        self.col=col
            
    def addSensors(self,sensors): 
        self.sensors.extend(sensors)
        if NUMPY:
            self.sensor_x1=len(sensors)*[0.0]
            self.sensor_y1=len(sensors)*[0.0]
            self.sensor_x2=len(sensors)*[0.0]
            self.sensor_y2=len(sensors)*[0.0]
                    
    def setController(self,controller):
       self.controller=controller
             
    def base_init(self):
        self.state=State() 
        self.state.ang=math.pi
        self.state.dangdt=0.0
        self.state.x=0.0
        self.state.y=0.0
        self.state.dxdt=0.0
        self.state.dydt=0.0
        self.state.vel=0.0
        self.state.collide=False
        self.state.collide_count=0
        self.state.age=0.0
        self.state.pos_trips=0
        self.state.neg_trips=0
        self.state.distance_travelled=0.0
     
    def update_sensors_todo_fixme(self):
        world=self.world
        state=self.state
        
        cnt=0
        for sensor in self.sensors:
            ang=sensor.ang_ref+state.ang
            sensor.ang=ang
            self.sensor_x1[cnt]=state.x
            self.sensor_y1[cnt]=state.y
            self.sensor_x2[cnt]=state.x+sensor.range*math.sin(ang)
            self.sensor_y1[cnt]=state.y+sensor.range*math.cos(ang)
            cnt+=1
            
        
        (s,wall)=world.find_closest_intersect2_vec(self.sensor_x1,self.sensor_y1,self.sensor_x2,self.sensor_y2)
        
        cnt=0
        for sensor in self.sensors:
            sensor.val=s[cnt]*sensor.range
            if wall[cnt] == None:
                sensor.wall=None
            else:
                sensor.wall=wall[cnt].name 
        
    def update_sensors(self):
        world=self.world
        state=self.state
        
        
        for sensor in self.sensors:
            ang=sensor.ang_ref+state.ang
            sensor.ang=ang
            (s,wall)=world.find_closest_intersect(state.x,state.y,state.x+sensor.range*math.sin(ang),state.y+sensor.range*math.cos(ang))

            sensor.val=s*sensor.range
            if wall == None:
                sensor.wall=None
            else:
                sensor.wall=wall.name


    def draw(self,screen):
        gui.draw_sensors(self,screen)
        gui.draw_pod(self,screen)

 

class CarPod(Pod):
 
    def __init__(self,col=(255,0,0)):
        Pod.__init__(self,col)
        self.init()
    
    def setColour(self,col):
        self.col=col
        
    def init(self):
        self.base_init()
        self.mass  = 10.
        self.brake = 0.
        self.steer_factor=.05
        self.thrust_max=200.
        self.slip_thrust_max=200.
        self.slip_speed_thresh=80.
        self.slip_speed_max=200
        self.slip=0.0
        self.damp=.0001
        #self.vel=0.0
        self.fuel=0.0
        self.state.distance_travelled=0.0
   
        
        
    def step(self,out):
        world=self.world
        dt=world.dt
        state=self.state
        #self.control=self.controller.process(self,dt)
        if out == None:
            return
       
        self.up=out[0] 
        self.down=0.0
        self.left=out[1]
        self.right=out[2]
        
        self.fuel -= self.up*dt
        self.state.age += dt
        
        #self.contr.limit()

        slipThrust = (self.up-self.down)*self.slip*self.slip_thrust_max
        state.dxdt = state.dxdt*self.slip+(1.0-self.slip)*state.vel*math.sin(state.ang) +  math.sin(state.ang)*slipThrust*dt
        state.dydt = state.dydt*self.slip+(1.0-self.slip)*state.vel*math.cos(state.ang) +  math.cos(state.ang)*slipThrust*dt
        #self.dxdt = self.vel*sin(self.ang)
        #self.dydt = self.vel*cos(self.ang)

        xNext = state.x + state.dxdt*dt
        yNext = state.y + state.dydt*dt

        wall,seg_pos=world.check_collide_with_wall(state.x,state.y,xNext,yNext)
        
        ang_prev=state.ang
        
        if wall == None:

            (p,n)=world.count_trips(state.x,state.y,xNext,yNext)
            state.pos_trips += p
            state.neg_trips += n
        
            #nprint self.pos_trips,self.neg_trips
            
            state.x = xNext
            state.y = yNext
            if state.vel > 0:
                damp_fact=state.vel*state.vel*state.vel/abs(state.vel)
            else:
                damp_fact=0
                
            state.vel += (self.up-self.down)*self.thrust_max/self.mass-self.damp*damp_fact
            state.collide = False
            state.ang += 0.5*(2.0-self.slip)*(-self.right+self.left)*state.vel*self.steer_factor*dt + self.slip*state.dangdt*dt
            avel=abs(state.vel)
            if avel > self.slip_speed_max:
                self.slip=1
            elif avel > self.slip_speed_thresh:
                t=(avel-self.slip_speed_thresh)/(self.slip_speed_max-self.slip_speed_thresh)
                self.slip=t
            else:
                self.slip=0

            

        else:
            state.seg_pos=seg_pos
            state.dydt = 0
            state.dxdt = 0
            state.vel  = 0
            state.collide = True
            state.ang += (-self.control.right+self.control.left)*state.vel*self.steer_factor*dt

        self.state.distance_travelled += math.sqrt(state.dxdt**2+state.dydt**2)*dt
        state.dangdt=(state.ang-ang_prev)/dt
 

class GravityPod(Pod):

    g = 2

    def __init__(self,col=(255,0,0)):
        Pod.__init__(self,col)
        self.init()
     
    def init(self):
        self.base_init()
        self.mass=2
        self.inertia=.5     # angluar inertia
        self.thrustMax=20
        self.spinThrustMax=.11
        #self.vel=0.0
        self.fuel=0.0
        self.distanceTravelled=0.0
        #self.age=0.0
        #self.pos_trips=0
        #self.neg_trips=0
        #self.collide=False

    def step(self,out,dt):

        
       
        
        # state=State(self)
       # self.control=self.controller.process(self,dt)
        if out == None:
            return
        
        
        self.up=out[0] 
        self.left=out[1]
        self.right=out[2]
        
        #self.control.limit()
        
        state=self.state
        
        state.age += dt
        xNext = state.x + state.dxdt*dt
        yNext = state.y + state.dydt*dt


#        
        state.x=xNext
        state.y=yNext
        thrust=self.thrustMax*self.up
        state.dydt += thrust*math.cos(state.ang)/self.mass+self.g
        state.dxdt += thrust*math.sin(state.ang)/self.mass

        state.ang    += state.dangdt*dt
        state.dangdt += (-self.right+self.left)*self.spinThrustMax/self.inertia




class SimplePod(Pod):

    def __init__(self,nSensor,sensorRange,col,stepSize=20):
        Pod.__init__(self,nSensor,sensorRange,col)
        self.stepSize=stepSize

    def step(self,dt,world):
        state=State(self)
        self.control=self.controller.process(self.sensors,state,dt)
        self.control.limit()

    
        xNext = state.x + self.stepSize*(self.control.right - self.control.left)
        yNext = state.y + self.stepSize*(self.control.down - self.control.up)

        wall=world.check_collide_with_wall(state.x,state.y,xNext,yNext)
        if wall == None:
            state.x=xNext
            state.y=yNext
            state.collide=False
        else:
            state.collide=True
            
class Misc:    
    def __init__(self):
        self.zoom=1.0
        

misc=Misc()


# Copyright (C) 2005  Jujucece <jujucece@gmail.com>
#
# This file is part of pyRacerz.
#
# pyRacerz is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyRacerz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyRacerz; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# Some mods by PJL
# Note I do not use a lot of the code below (I left it there in case I wanted to do so in future)


class SpriteCar(CarPod,pygame.sprite.Sprite):
  '''Class representing the car belonging to a player'''

    
  def __init__(self):
      self.inited=False
      Pod.__init__(self,col=(255,0,0))
      self.image_file=None
      # need to delay initialisation until py is up and running
    
  def set_image(self,file):
       self.image_file=os.path.abspath(file)
       #print "spritepath=",self.image_file
      
  def do_init(self):
    if self.image_file == None:
        return
    
    self.inited=True
    # print "Hello form Sprite init "
    color='1'
    level=1
      
    pygame.sprite.Sprite.__init__(self)
    image = pygame.image.load(self.image_file).convert_alpha()
    # impygame.image.load(os.path.join("sprites", "car" + str(color) + ".png")).convert_alpha()
    #imageLight = pygame.image.load(os.path.join("sprites", "car" + str(color) + "B.png")).convert_alpha()
    
    self.sprite = pygame.sprite.RenderPlain(self)

    self.miniCar = pygame.transform.rotozoom(image, 0, misc.zoom)

    self.color = color

    if level > 3:
      level = 3
    if level < 1:
      level = 1

    self.level = level # 1,2,3

    if level == 1:
      self.maxSpeed = 3.5
    if level == 2:
      self.maxSpeed = 4.5
    if level == 3:
      self.maxSpeed = 6

    self.maxSpeedB = -0.66*self.level
    self.power = 0.0133*self.level

    self.sizeRect = int(30*misc.zoom)

    # TODO do not put it hardcoded...
    self.width = int(15*misc.zoom)
    self.height = int(24*misc.zoom)
    self.blitXoffset=self.sizeRect/2
    self.blitYoffset=self.sizeRect/2
    
    self.cars = []
    #self.cars2 = []

    # For the 256 angle
    for j in range(0,256):
      
      # Rotate car without and with Red Light
      carRot=pygame.Surface((self.sizeRect,self.sizeRect), SRCALPHA|HWSURFACE, 16).convert_alpha()
      #carRotLight=pygame.Surface((self.sizeRect,self.sizeRect), SRCALPHA|HWSURFACE, 16).convert_alpha()
      carRot2=pygame.Surface((self.sizeRect,self.sizeRect), SRCALPHA|HWSURFACE, 16).convert_alpha()
     # carRotLight2=pygame.Surface((self.sizeRect,self.sizeRect), SRCALPHA|HWSURFACE, 16).convert_alpha()

      carRotRaw=pygame.transform.rotozoom(image, -j*360.0/256.0, misc.zoom)
      #carRotLightRaw=pygame.transform.rotozoom(imageLight, -j*360.0/256.0, misc.zoom)

      carRot.blit(carRotRaw, ((self.sizeRect-carRotRaw.get_width())/2, (self.sizeRect-carRotRaw.get_height())/2) )
     # carRotLight.blit(carRotLightRaw, ((self.sizeRect-carRotLightRaw.get_width())/2, (self.sizeRect-carRotLightRaw.get_height())/2) )

      # Create the car shadow
      # It's surely possible to use a better method with a mask, but...
      carRotShade = carRot.copy()
      for x in range(0, carRotShade.get_width()):
        for y in range(0, carRotShade.get_height()):
         if carRotShade.get_at((x, y)) != (0,0,0,0):
           carRotShade.set_at((x, y), (50,50,50,100))

      carRot2.blit(carRotShade, (2,1))
      carRot2.blit(carRot, (0,0))
     # carRotLight2.blit(carRotShade, (2,1))
      #carRotLight2.blit(carRotLight, (0,0))

      self.cars.append(carRot2)
      #print carRot2.get_width(),carRot2.get_height()
      
     # self.cars2.append(carRotLight2)

      self.x = 0
      self.y = 0
      self.ox = 0
      self.oy = 0
      self.rect = pygame.Rect(int(self.x-self.sizeRect/2),int(self.y-self.sizeRect/2),self.sizeRect,self.sizeRect)
      self.movepos = [0.0,0.0]

  def reInit(self, track, rank):
    self.track = track

    # Blink is used to warn the player
    self.blink = 0
    self.blinkCount = 0

    # Rank is only used by the car to initilaize itself
    if rank == 0:
      self.x = 0
      self.y = 0
      self.ox = 0
      self.oy = 0
    elif rank == 1:
      self.x = track.startX1
      self.y = track.startY1
      self.ox = track.startX1
      self.oy = track.startY1
    elif rank == 2:
      self.x = track.startX2
      self.y = track.startY2
      self.ox = track.startX2
      self.oy = track.startY2
    elif rank == 3:
      self.x = track.startX3
      self.y = track.startY3
      self.ox = track.startX3
      self.oy = track.startY3
    else:
      # Side 1
      if rank%2 == 1:
        precX = track.startX3
        precY = track.startY3
        # Compute all positions from 3 to find the good one !
        for i in range(3, rank, 2):
          precX = precX + (track.startX2 - track.startX1)
          precY = precY + (track.startY2 - track.startY1)
          precX = precX + (track.startX3 - track.startX2)
          precY = precY + (track.startY3 - track.startY2)
      # Side 2
      else:
        precX = track.startX2
        precY = track.startY2
        # Compute all positions from 2 to find the good one !
        for i in range(2, rank, 2):
          precX = precX + (track.startX3 - track.startX2)
          precY = precY + (track.startY3 - track.startY2)
          precX = precX + (track.startX2 - track.startX1)
          precY = precY + (track.startY2 - track.startY1)
      self.x = precX
      self.y = precY
      self.ox = precX
      self.oy = precY

    self.rect = pygame.Rect(int(self.x-self.sizeRect/2),int(self.y-self.sizeRect/2),self.sizeRect,self.sizeRect)
    self.listCarRect = (self.rect, self.rect, self.rect, self.rect)

    self.angle = track.startAngle
    self.oldAngle = track.startAngle

    self.angleW = 0.0
    self.brake = 0.0
    self.throttle = 0.0

    self.speed = 0.0
    self.accel = 0.0

    # Only useful for Collisions
    self.newSpeed = 0

    self.speedR = 0.0
    self.accelR = 0.0

    self.speedL = 0.0
    self.accelL = 0.0

    self.movepos = [0.0,0.0]

  def update(self):
    ''' Function called at each frame to update car sprite...
    It's the main computation method for car movement !'''
   
    # Get the 4 important point of the car ~ 4 wheels
    coordN = (self.x - math.cos(self.angle)*self.height/2, self.y - math.sin(self.angle)*self.height/2)
    coordS = (self.x + math.cos(self.angle)*self.height/2, self.y + math.sin(self.angle)*self.height/2)
    coordE = (self.x + math.cos(math.pi/2.0-self.angle)*self.width/2, self.y - math.sin(math.pi/2.0-self.angle)*self.width/2)
    coordW = (self.x - math.cos(math.pi/2.0-self.angle)*self.width/2, self.y + math.sin(math.pi/2.0-self.angle)*self.width/2)
    coord0 = (int(coordN[0] - math.sin(self.angle)*self.width/2), int(coordN[1] + math.cos(self.angle)*self.width/2))
    coord1 = (int(coordN[0] + math.sin(self.angle)*self.width/2), int(coordN[1] - math.cos(self.angle)*self.width/2))
    coord2 = (int(coordS[0] - math.sin(self.angle)*self.width/2), int(coordS[1] + math.cos(self.angle)*self.width/2))
    coord3 = (int(coordS[0] + math.sin(self.angle)*self.width/2), int(coordS[1] - math.cos(self.angle)*self.width/2))

    #misc.screen.set_at(coord0, (255,0,255))
    #misc.screen.set_at(coord1, (255,0,255))
    #misc.screen.set_at(coord2, (255,0,255))
    #misc.screen.set_at(coord3, (255,0,255))

    # Construct the 4 Rects useful for collisions
    minXX = min(coord0[0], coord1[0], self.x)
    maxXX = max(coord0[0], coord1[0], self.x)
    minYY = min(coord0[1], coord1[1], self.y)
    maxYY = max(coord0[1], coord1[1], self.y)
    carRectN = (minXX, minYY, maxXX - minXX, maxYY - minYY)
    
    minXX = min(coord2[0], coord3[0], self.x)
    maxXX = max(coord2[0], coord3[0], self.x)
    minYY = min(coord2[1], coord3[1], self.y)
    maxYY = max(coord2[1], coord3[1], self.y)
    carRectS = (minXX, minYY, maxXX - minXX, maxYY - minYY)
    
    minXX = min(coordE[0], self.x)
    maxXX = max(coordE[0], self.x)
    minYY = min(coordE[1], self.y)
    maxYY = max(coordE[1], self.y)
    carRectE = (minXX, minYY, maxXX - minXX, maxYY - minYY)
    
    minXX = min(coordW[0], self.x)
    maxXX = max(coordW[0], self.x)
    minYY = min(coordW[1], self.y)
    maxYY = max(coordW[1], self.y)
    carRectW = (minXX, minYY, maxXX - minXX, maxYY - minYY)
    
    self.listCarRect = (carRectN, carRectS, carRectE, carRectW)

    #pygame.draw.rect(misc.screen, (255, 0, 0), self.listCarRect[0])
    #pygame.draw.rect(misc.screen, (0, 255, 0), self.listCarRect[1])
    #pygame.draw.rect(misc.screen, (0, 0, 255), self.listCarRect[2])
    #pygame.draw.rect(misc.screen, (255, 0, 255), self.listCarRect[3])

    #misc.screen.set_at(coordN, (255,255,0))
    #misc.screen.set_at(coordS, (255,255,0))
    #misc.screen.set_at(coordE, (255,255,0))
    #misc.screen.set_at(coordW, (255,255,0))
    
    if min(coord0) < 0 or coord0[0] > 1023*misc.zoom or coord0[1] > 767*misc.zoom:
      g0 = 0
    else:
      g0 = self.track.trackF.get_at(coord0)[1]
    if min(coord1) < 0 or coord1[0] > 1023*misc.zoom or coord1[1] > 767*misc.zoom:
      g1 = 0
    else:
      g1 = self.track.trackF.get_at(coord1)[1]
    if min(coord2) < 0 or coord2[0] > 1023*misc.zoom or coord2[1] > 767*misc.zoom:
      g2 = 0
    else:
      g2 = self.track.trackF.get_at(coord2)[1]
    if min(coord3) < 0 or coord3[0] > 1023*misc.zoom or coord3[1] > 767*misc.zoom:
      g3 = 0
    else:
      g3 = self.track.trackF.get_at(coord3)[1]

    g = (g0 + g1 + g2 + g3)/4.0

    #self.crashFlag=0

    # Compute Accel
    # - Accel depends only on present datas
    self.accel=self.power*(1.0*self.throttle-1.7*self.brake)*(g/255.0)

    # Engine brake
    if self.throttle == 0.0 and self.speed > 0:
      self.accel = self.accel - 0.005
    if self.throttle == 0.0 and self.speed < 0:
      self.accel = self.accel + 0.005

    oldSpeed = self.speed

    # Compute Speed
    # - Acceleration acts on the Speed
    self.speed=self.speed+self.accel

    # Max back speed
    if self.speed <= self.maxSpeedB*(g/255.0):
      self.speed = self.maxSpeedB*(g/255.0)
      self.accel = 0

    # Max speed
    if self.speed >= self.maxSpeed*(g/255.0):
      self.speed = self.maxSpeed*(g/255.0)
      self.accel = 0
    
    # If speed is very slow, stop the car
    if self.speed < 0.005 and self.speed > -0.005:
      self.accel = 0.0
      self.speed = 0.0

    # Compute Rotational Speed

    # - Rotational Accel depends only on present datas
    self.accelR=self.angleW*0.007

    # Take in account of rotating of the oversteering at braking
    # - Only acting when the car is braking hard
    # - Acting on the the Rotational Acceleration
    # - Memory because accelR is used the frame after
    # - Depending on the braking power (accel < 0)
    if self.accel < -self.power*1.7*(2.0/3) and self.accelR > 0 and self.speed > self.maxSpeed*(2.0/3):
      self.accelR = self.accelR + abs(self.accel)*0.08
    elif self.accel < -self.power*1.7*(2.0/3) and self.accelR < 0 and self.speed > self.maxSpeed*(2.0/3):
      self.accelR = self.accelR - abs(self.accel)*0.08
    
    # Take in account of understeering at acceleration
    # - Not acting when braking
    # - Acting on accelR
    #if (self.accel >= 0 and self.speed > self.maxSpeed*(2.0/3)) and ((self.speedL > 0.6 and oldSpeedL > 0.6) or (self.speedL < -0.6 and oldSpeedL < -0.6)):
    #if (self.accel >= 0 and self.speed > self.maxSpeed*(2.0/3)) and (self.speedL > 0.6 or self.speedL < -0.6):
    #if self.accel >= 0:# and self.accelR > 0:
    #  self.accelR = self.accelR

    if self.speed >= 0:
      self.speedR=0.8*self.speedR+self.accelR
    else:
      self.speedR=0.8*self.speedR-self.accelR

    # If the rotation is slow, stop the rotation
    if self.speedR < 0.003 and self.speedR > -0.003:
      self.accelR = 0.0
      self.speedR = 0.0

    oldoldAngle = self.oldAngle

    self.oldAngle = self.angle
    
    self.angle=self.angle+self.speedR

    # Take in account of the oversteering at acceleration
    # - Only acting when power is at the maximum
    # - No memory so it's only acting on the angle
    # - More the speed is near the max less this is effecting
    if self.accel == self.power and self.speed > 0:
      self.angle = self.angle + 0.1*self.speedR*(1.5*self.maxSpeed-self.speed)

    # Compute Lateral Speed

    # The lateral acceleration is calculated with the 2 angle
    # - Lateral Accel depends only on present datas
    # - The formula is Flat = M v^2  / radius where radius=L/sin(angle)
    if self.angle-self.oldAngle != 0:
      radius = math.sqrt(math.pow((self.ox - self.x)/misc.zoom, 2) + math.pow((self.oy - self.y)/misc.zoom, 2))/math.sin(self.angle-self.oldAngle)
      if radius > 2000 or radius < -2000 or (radius < 1 and radius > -1):
        self.accelL = 0
      else:
        self.accelL = 5*self.speed*self.speed/radius
    else:
      self.accelL = 0

    # Take in account of sliding of the oversteering at braking
    # - Acting on speed and accelL to simulate lateral sliding
    # - Only acting when the braking is hard
    # - The accelL augmentation is based on accel (compared to the max accel)
    if self.accel < -self.power*1.7*(2.0/3) and self.speed > 0:
      self.accelL = self.accelL * (1 + 1.3*abs(self.accel)/(1.7*self.power))
      self.speed = self.speed - abs(0.6*self.accel)

    self.speedL = 0.2*self.speedL + self.accelL

    # If the speed is too slow
    if self.speedL < 0.003 and self.speedL > -0.003:
      self.speedL = 0.0

    # Make some corrections
    if self.angle<0: 
      self.angle=self.angle+2.0*math.pi
    if self.angle>2.0*math.pi:
      self.angle=self.angle-2.0*math.pi;

    oldoldx = self.ox
    oldoldy = self.oy
    self.ox = self.x
    self.oy = self.y

    self.speed = self.speed*misc.zoom
    self.speedL = self.speedL*misc.zoom
    self.speedR = self.speedR*misc.zoom
    
    if self.speedL > 0.0:
      self.x = self.x - math.cos(self.angle-math.acos(self.speed/math.sqrt(self.speed*self.speed+self.speedL*self.speedL)))*math.sqrt(self.speed*self.speed+self.speedL*self.speedL)
      self.y = self.y - math.sin(self.angle-math.acos(self.speed/math.sqrt(self.speed*self.speed+self.speedL*self.speedL)))*math.sqrt(self.speed*self.speed+self.speedL*self.speedL)
    elif self.speedL < 0.0:
      self.x = self.x - math.cos(self.angle+math.acos(self.speed/math.sqrt(self.speed*self.speed+self.speedL*self.speedL)))*math.sqrt(self.speed*self.speed+self.speedL*self.speedL)
      self.y = self.y - math.sin(self.angle+math.acos(self.speed/math.sqrt(self.speed*self.speed+self.speedL*self.speedL)))*math.sqrt(self.speed*self.speed+self.speedL*self.speedL)
    else:
      self.x=self.x-math.cos(self.angle)*self.speed
      self.y=self.y-math.sin(self.angle)*self.speed

    self.speed = self.speed/misc.zoom
    self.speedL = self.speedL/misc.zoom
    self.speedR = self.speedR/misc.zoom

    # Collision -> move to the last Nice position
    #if self.track.track.get_rect().contains(self.rect) == False:
    if (self.x < 16*misc.zoom or self.x > 1024*misc.zoom-14*misc.zoom or self.y < 16*misc.zoom or self.y > 768*misc.zoom-14*misc.zoom) or g0 == 0 or g1 == 0 or g2 == 0 or g3 == 0:
      self.x = oldoldx
      self.y = oldoldy
      self.angle = oldoldAngle
      self.speed = -0.2*oldSpeed
      self.speedL = 0

    #print math.sqrt((self.x-self.ox)*(self.x-self.ox)+(self.y-self.oy)*(self.y-self.oy))

    self.movepos[0]=int(self.x) - int(self.ox)
    self.movepos[1]=int(self.y) - int(self.oy)

    self.rect.move_ip(self.movepos)
    #self.rect=pygame.Rect(int(self.x-self.sizeRect/2), int(self.y-self.sizeRect/2), self.sizeRect, self.sizeRect)

    if self.rect != (int(self.x-self.sizeRect/2), int(self.y-self.sizeRect/2), self.sizeRect, self.sizeRect):
      print "PROBLEM"
      print self.rect
      print self.x
      print self.y

    self.slide = 0
    # Compute tires slide
    if (self.accel >= 0.015 and self.speed <= 2 and self.speed>0) or self.accelL > 0.4 or self.accelL < -0.4:
      self.slide = 1
    # If the car is braking, the slide is larger
    if self.accel < -0.005:
      self.slide = 2
    
    #print self.movepos
    #print "xy %f %f %f thbr %f %f aW %f s %f acc %f sR %f accR %f spdL %f accelL %f " \
    #  % (self.x, self.y, self.angle, self.brake, self.throttle, self.angleW, self.speed, self.accel, self.speedR, self.accelR, self.speedL, self.accelL)

  def doAccel(self):
    self.throttle=self.throttle+0.1
    if self.throttle>1:
      self.throttle=1

  def noAccel(self):
    self.throttle=self.throttle-0.05
    if self.throttle<0:
      self.throttle=0

  def doBrake(self):
    self.brake=self.brake+0.2
    if self.brake>1:
      self.brake=1

  def noBrake(self):
    self.brake=0

  def doLeft(self):
    self.angleW=self.angleW-0.2
    if self.angleW < -1:
      self.angleW = -1

  def doRight(self):
    self.angleW=self.angleW+0.2
    if self.angleW > 1:
      self.angleW = 1

  def noWheel(self):
    self.angleW = 0.0 

 
  def draw(self,screen):
    if not self.inited:
        self.do_init()
        
        
    gui.draw_sensors(self,screen)
    
    
    if self.image_file == None:
        gui.draw_pod(self,screen)
    else:
        index=(255-64-int(self.state.ang*256/math.pi/2.0))%256
        screen.blit(self.cars[index],(self.state.x-self.blitXoffset,self.state.y-self.blitYoffset))
        gui.draw_pod_state(self,screen)
        
        


