from pod.pods import Sensor,gui

def equip_car(pod):
    #  no sensors yet
    return
 
    
 
def controller(pod,control):   
    keys=gui.get_pressed()
    
    #http://thepythongamebook.com/en:glossary:p:pygame:keycodes
    if keys[gui.keys.K_UP]:
        control.up=0.5
    else:
        control.up=.0
          
    if keys[gui.keys.K_DOWN]:
        control.down=0.5
    else:
        control.down=.0
        
    if keys[gui.keys.K_LEFT]:
        control.left=.1
    else:
        control.left=.0
  
    if keys[gui.keys.K_RIGHT]:
        control.right=.1
    else:
        control.right=.0
        