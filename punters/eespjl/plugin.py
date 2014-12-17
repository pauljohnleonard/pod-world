#  PJLs example submission

from pod.pods import Sensor,gui

class MyData:
    
    def __init__(self):
        pass
    
    
def equip_car(pod):
          
          
    sensors=[Sensor(angle=0.4,name="Left"),Sensor(angle=-0.4,name="Right")]
    pod.addSensors(sensors) 
    pod.col=(0,255,225)


    pod.data=MyData()
    pod.data.pram=[100,0.5]      #   USER DATA CAN BE ANYTHING YOU WANT!
    pod.poly=[(-10,-10),(-5,20),(5,20),(10,-10)]
    
    
def controller(pod):
   
    vel=pod.state.vel
    control=pod.control


    if vel < pod.data.pram[0]:
        control.up=pod.data.pram[1]
    else:
        control.up=0.0
       
       
    left=pod.sensors[0].val
    right=pod.sensors[1].val
    
    #print left,right
    
    if left < right:
        control.left=0
        control.right=.1  
    else:
        control.left=.1
        control.right=0
        
    


    