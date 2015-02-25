"""
GUI routines
"""

import pygame
import fontmanager
import math


keys=pygame
 
red=(255,0,0)
dim_window=0
 
def Rect(a,b,c,d):
    return pygame.Rect(a,b,c,d)


def init_surface(dim_world,run_name):  
        pygame.init()
        modes=pygame.display.list_modes()
        global dim_window
        dim_display=modes[0]
        global fontMgr,display,dim_window
        sx=dim_display[1]/float(dim_world[1])
        sy=dim_display[0]/float(dim_world[0])
        
        if sx < 1 or sy < 1:
            s=min(sx,sy)/1.2
            dim_window=(dim_world[0]*s,dim_world[1]*s)
            print "Small screen: scaling world by ",s

        else: 
            dim_window=dim_world

        display = pygame.display.set_mode(dim_window)
        pygame.display.set_caption(run_name+'(press escape to exit)')
        #fontMgr = fontmanager.cFontManager(((None, 16),(None, 20), (None, 48), ('helvetica', 24)))
        fontMgr = fontmanager.cFontManager((('Courier New', 12),('Courier New', 16), ('Courier New', 24), ('Courier New', 48)))
        return pygame.Surface(dim_world) #
 
def get_pressed():
    kk=pygame.key.get_pressed()
    return kk

def draw_string(screen,str1,point,col,size ):
    fontMgr.Draw(screen, 'Courier New', size,str1,point, col) 


def clock():    
    return pygame.time.Clock() 

def check_for_quit():
    keyinput = get_pressed()
                
    if keyinput[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
                pygame.display.quit()
                return True
            
    return False
            
def grab_events():
    pygame.event.pump()
               
def blit(screen):
        zz=pygame.transform.scale(screen,dim_window)
        display.blit(zz,(0,0))
        pygame.display.flip()
        
def draw_line(screen,x1,y1,x2,y2,col,thick):
    pygame.draw.line(screen,col,(x1,y1),(x2,y2),thick)
 
 
def fill_circle(screen,x1,y1,rad,col):
    pygame.draw.circle(screen,col,(int(x1),int(y1)),rad)
    
    
#
# Following routines are not used for the IP world
#
       
def draw_world(world,screen):
        if not world.blind:
            for wall in world.walls:
                if "start" in wall.name:
                    col=(255,255,0)
                elif "end" in wall.name:
                    col=(0,255,255)
                else:
                    col=(0,0,255)

                for seg in wall.segments:
                    pygame.draw.line(screen,col,(seg[0],seg[1]),(seg[2],seg[3]),6)
        
            col=(100,30,30)
            for t in world.trips:
                pygame.draw.line(screen,col,(t[0],t[1]),(t[2],t[3]),2)
                
        
        
        for pod in world.pods:
            pod.draw(screen)
                # raise SystemExit

def draw_pod(pod, screen):
        
        state=pod.state
        
        if state.collide:
            state.collide_count=100

        outline=util.rotate_poly(pod.pod_poly_ref, state.ang, state)
        
        if state.collide_count>0:
            col=(255,100,100)
            state.collide_count -= 1
        else:
            col=pod.col
        pygame.draw.polygon(screen,col,outline)
        
        if pod.control == None:
            return
        
        if pod.control.up > 0.0:
            outline=util.rotate_poly(pod.thrust_poly_ref, state.ang, state)
            pygame.draw.polygon(screen,(255*pod.control.up,0,0),outline)
        if pod.control.left > 0.0:
            outline=util.rotate_poly(pod.left_poly_ref, state.ang, state)
            pygame.draw.polygon(screen,(255*pod.control.left,0,0),outline)
        if pod.control.right > 0.0:
            outline=util.rotate_poly(pod.right_poly_ref, state.ang, state)
            pygame.draw.polygon(screen,(255*pod.control.right,0,0),outline)


def draw_pod_state(pod, screen):
        
        state=pod.state
        
        if state.collide:
            state.collide_count=100

        
        if pod.control == None:
            return
        
        if pod.control.up > 0.0:
            outline=util.rotate_poly(pod.thrust_poly_ref, state.ang, state)
            pygame.draw.polygon(screen,(255*pod.control.up,255*pod.control.up,0),outline)
        if pod.control.left > 0.0:
            outline=util.rotate_poly(pod.left_poly_ref, state.ang, state)
            pygame.draw.polygon(screen,(0,255*pod.control.left,0),outline)
        if pod.control.right > 0.0:
            outline=util.rotate_poly(pod.right_poly_ref, state.ang, state)
            pygame.draw.polygon(screen,(0,255*pod.control.right,0),outline)
        if pod.control.down > 0.0:
            outline=util.rotate_poly(pod.brake_poly_ref, state.ang, state)
            pygame.draw.polygon(screen,(255*pod.control.down,0,255*pod.control.down),outline)
            
            
def draw_sensors(pod,screen):
        
        state=pod.state
        for sensor in pod.sensors:
            wallName=sensor.wall
            if wallName== None:
                col=(10,10,10)
            elif "end" in wallName:
                col=(255,255,255)
            else:
                col=(70,70,70)

            dist=sensor.val
            
            p1=(state.x,state.y)
            p2=(state.x+dist*math.sin(sensor.ang),state.y+dist*math.cos(sensor.ang))
            pygame.draw.line(screen,col,p1,p2,1)
