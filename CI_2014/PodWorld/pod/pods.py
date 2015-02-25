'''
Created on 21 Dec 2010

@author: pjl
'''
from config import *

if NUMPY:
    import numpy
    
import math
import util
import gui_base as gui
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
        
    def __repr__(self):
        txt=""
        for attr, value in self.__dict__.iteritems():
            txt+=str(attr)+ " "+ str(value)+"\n" 
     
        return txt
    
class Sensor:
    """  
        angle:  anticlockwise angle from forward 
        range:  
        name:
    """
           
    def __init__(self,angle,range=20000,name="Sensor"):
       
        
        self.ang_ref=angle
        self.ang=angle
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
    

    def __init__(self,world,col):
        
        self.world=world
        self.message="init"
       # self.control=Control()
        self.sensors=[]
       # self.base_init()    
        self.col=col
        if world != None:
            world.init_pod(self)
        self.poly=Pod.pod_poly_ref
          
    #
    def setWorld(self,world):
        self.world=world
        self.reset()
        
    def reset(self): 
        self.world.init_pod(self)
         
    def addSensors(self,sensors): 
        self.sensors.extend(sensors)
        if NUMPY:
            self.sensor_x1=len(sensors)*[0.0]
            self.sensor_y1=len(sensors)*[0.0]
            self.sensor_x2=len(sensors)*[0.0]
            self.sensor_y2=len(sensors)*[0.0]
        self.update_sensors()    
              
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
        self.state.slip=0.0
        
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
           # print "VAL=",sensor.val

    def draw(self,screen):
        gui.draw_sensors(self,screen)
        gui.draw_pod(self,screen)

 

class CarPod(Pod):
 
    def __init__(self,world,col=(255,0,0)):
        Pod.__init__(self,world,col)
        self.control=None
        
    def setColour(self,col):
        self.col=col
        
    def init(self):
        self.base_init()
        self.mass  = 10.
       # self.brake = 0.
        self.steer_factor=.2
        self.thrust_max=200.
        self.slip_thrust_max=100.
        self.slip_speed_thresh=100.
        self.slip_speed_max=200.
        
        self.damp=.0001
        #self.vel=0.0
        self.fuel=0.0
        self.state.distance_travelled=0.0
   
        
        
    def step(self,control):
        
        world=self.world
        dt=world.dt
        state=self.state
        self.control=control
        
        #self.fuel -= self.control.up*dt
        self.state.age += dt
        
        self.control.limit()

        slipThrust = (self.control.up-self.control.down)*self.state.slip*self.slip_thrust_max
        
        state.dxdt = state.dxdt*self.state.slip+(1.0-self.state.slip)*state.vel*math.sin(state.ang) +  math.sin(state.ang)*slipThrust*dt
        state.dydt = state.dydt*self.state.slip+(1.0-self.state.slip)*state.vel*math.cos(state.ang) +  math.cos(state.ang)*slipThrust*dt
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
            if state.vel > 0.001:
                damp_fact=state.vel*state.vel*state.vel/abs(state.vel)
            else:
                damp_fact=0.0
                
            state.vel += (self.control.up-self.control.down)*self.thrust_max/self.mass-self.damp*damp_fact
            state.collide = False
        
           # if state.age < 0.06:
           #     print 'X:',self.state.slip,self.control.right,self.control.left,state.vel,self.steer_factor,dt,state.dangdt
           #     print self.sensors[0].val,self.sensors[1].val
                
            state.ang += 0.5*(2.0-self.state.slip)*(-self.control.right+self.control.left)*state.vel*self.steer_factor*dt+ self.state.slip*state.dangdt*dt*.2
            avel=abs(state.vel)
            if avel > self.slip_speed_max:
                self.state.slip=1.0
            elif avel > self.slip_speed_thresh:
                t=(avel-self.slip_speed_thresh)/(self.slip_speed_max-self.slip_speed_thresh)
                self.state.slip=t
            else:
                self.state.slip=0.0

            

        else:
       
            
            state.seg_pos=seg_pos
            state.dydt = 0.0
            state.dxdt = 0.0
            state.vel  = 0.0
            state.collide = True
            state.ang += (-self.control.right+self.control.left)*state.vel*self.steer_factor*dt

        self.state.distance_travelled += math.sqrt(state.dxdt**2+state.dydt**2)*dt
        state.dangdt=(state.ang-ang_prev)/dt
        self.update_sensors()
        
 
