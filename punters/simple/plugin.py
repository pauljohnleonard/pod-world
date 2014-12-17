from pod.pods import Sensor,gui

def equip_car(pod):
          
    sensors=[Sensor(angle=0.4,name="Left"),Sensor(angle=-0.4,name="Right")]
    pod.addSensors(sensors) 
    pod.col=(0,255,225)
    pod.data=[200,0.5]      #   USER DATA CAN BE ANYTHING YOU WANT!
 
def controller(pod,control):   
   
    vel=pod.state.vel
    
    if vel < pod.data[0]:
        control.up=pod.data[1]
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
        
    


    