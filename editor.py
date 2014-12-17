#  Edit the next 2 variables if you wish.


FILE_NAME="worlds/bravenew.world"
DEFAULT_WIDTH=100
WINDOW_SIZE=(1000,800)
#--------------

import pygame
import math,time
import sys

 
background_col=(0,0,0)

 
class cFontManager:
    '''
    A simple class used to manage Font objects and provide a simple way to use
    them to draw text on any surface.
 
    Directly import this file to use the class, or run this file from the
    command line to see a trivial sample.
 
    Written by Scott O. Nelson  
    '''
    def __init__(self, listOfFontNamesAndSizesAsTuple):
        '''
        Pass in a tuple of 2-item tuples.  Each 2-item tuple is a fontname / 
        size pair. To use the default font, pass in a None for the font name.
        Font objects are created for each of the pairs and can then be used
        to draw text with the Draw() method below.
        
        Ex: fontMgr = cFontManager(((None, 24), ('arial', 18), ('arial', 24),
            ('courier', 12), ('papyrus', 50)))
 
        TODO: add support for bold & italics
        '''
        self._fontDict = {}
        for pair in listOfFontNamesAndSizesAsTuple:
            assert len(pair) == 2, \
                "Pair must be composed of a font name and a size - ('arial', 24)"
            if pair[0]:
                fontFullFileName = pygame.font.match_font(pair[0])
                assert fontFullFileName,'Font: %s Size: %d is not available.' % pair
            else:
                fontFullFileName = None # use default font
            self._fontDict[pair] = pygame.font.Font(fontFullFileName, pair[1])
 
    def Draw(self, surface, fontName, size, text, rectOrPosToDrawTo, color,
            alignHoriz='left', alignVert='top', antialias=False):
        '''
        '''
        pair = (fontName, size)
        assert pair in self._fontDict, \
            'Font: %s Size: %d is not available in cFontManager.' % pair
        fontSurface = self._fontDict[(fontName, size)].render(text,
            antialias, color)
        if isinstance(rectOrPosToDrawTo, tuple):
            surface.blit(fontSurface, rectOrPosToDrawTo)
        elif isinstance(rectOrPosToDrawTo, pygame.Rect):
            fontRect = fontSurface.get_rect()
            # align horiz
            if alignHoriz == 'center':
                fontRect.centerx = rectOrPosToDrawTo.centerx
            elif alignHoriz == 'right':
                fontRect.right = rectOrPosToDrawTo.right
            else:
                fontRect.x = rectOrPosToDrawTo.x  # left
            # align vert
            if alignVert == 'center':
                fontRect.centery = rectOrPosToDrawTo.centery
            elif alignVert == 'bottom':
                fontRect.bottom = rectOrPosToDrawTo.bottom
            else:
                fontRect.y = rectOrPosToDrawTo.y  # top
                
            surface.blit(fontSurface, fontRect)
 
def init_surface(dim_world):  
        global clock,screen,display
        global fontMgr,dim_window
        pygame.init()
        modes=pygame.display.list_modes()
        dim_display=modes[0]
        sx=dim_display[1]/float(dim_world[1])
        sy=dim_display[0]/float(dim_world[0])
        
        if sx < 1 or sy < 1:
            s=min(sx,sy)/1.2
            dim_window=(int(dim_world[0]*s),int(dim_world[1]*s))
            print "Small screen: not supported ",s
            sys.exit(0)
        else: 
            dim_window=dim_world

        display = pygame.display.set_mode(dim_window)
        pygame.display.set_caption('DR PJs  race track editor V-0.0.1-pre-alpha')
        fontMgr = cFontManager(((None, 12),(None, 14),(None, 16),(None, 18),(None, 20), (None, 48), ('helvetica', 24)))
        screen=pygame.Surface(dim_world) #
 
def get_pressed():
    kk=pygame.key.get_pressed()
    
    return kk

def draw_string(screen,str1,point,col,size ):
    
    
    toks=str1.split("\n")
    x=point[0]
    y=point[1]
    for line in toks:
        fontMgr.Draw(screen, None, size,line,(x,y), col)
        y+=(size+2) 

def check_for_quit():
    keyinput = get_pressed()
                
    if keyinput[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
                pygame.display.quit()
                return True
            
    return False
       
def clear_screen():
    screen.fill(background_col)  
         
def grab_events():
    pygame.event.pump()
               
def blit(screen):
        zz=pygame.transform.scale(screen,dim_window)
        display.blit(zz,(0,0))
        pygame.display.flip()
           
def draw_line(screen,x1,y1,x2,y2,col,thick):
    pygame.draw.line(screen,col,(x1,y1),(x2,y2),thick)
    
def draw_points(pts,screen,close):
    ptLast=None
    col=(255,255,0)
    
    if len(pts) > 1:
        for pt in pts:
            
            if ptLast != None:
                pygame.draw.line(screen,col,ptLast,pt,6)
            ptLast=pt
    
        if close:
            pygame.draw.line(screen,col,pts[-1],pts[0],6)
         
        
    col=(0,255,255)
    for pt in pts:        
        pygame.draw.circle(screen,col,pt,6)


   
def draw_trips(pts,pts2,screen):
    ptLast=None
    col=(155,55,155)
    for a,b in zip(pts,pts2):    
         pygame.draw.line(screen,col,a,b,4)
        
                
def get_stuff():
    pos=pygame.mouse.get_pos()
    but=pygame.mouse.get_pressed()
    kk=pygame.key.get_pressed()
    return but,[pos[0],pos[1]],kk
        
def pause():
    time.sleep(0.3)
   

def dir(a,b):
    dx=b[0]-a[0]
    dy=b[1]-a[1]
    dd=math.sqrt(dx*dx+dy*dy)
    if dd <= 0.0:
        return None
    return (dx/dd,dy/dd)
   
def add(vec1,vec2):
    return (vec1[0]+vec2[0],vec1[1]+vec2[1]) 

def find_nearest(pts,pos):
    d=1e32
    for pt in pts:
        dx=pt[0]-pos[0]
        dy=pt[1]-pos[1]
        dd=dx*dx+dy*dy
        if dd < d:
            ptRet=pt
            d=dd
    return ptRet


        
def rotate_poly(poly,ang,pos):
    ret=[]
    for p1 in poly:
        x=p1[0]*math.cos(ang)+p1[1]*math.sin(ang)+pos[0]
        y=-p1[0]*math.sin(ang)+p1[1]*math.cos(ang)+pos[1]
        ret.append((x,y))
    return ret

def draw_pod(pos,ang, screen,col):       
          
        pod_poly_ref=[(-10,-10),(0,20),(10,-10)]
        outline=rotate_poly(pod_poly_ref, ang, pos)
    
        pygame.draw.polygon(screen,col,outline)
            
            
 

def draw_string(screen,str1,point,col,size ):
    
    
    toks=str1.split("\n")
    x=point[0]
    y=point[1]
    for line in toks:
        fontMgr.Draw(screen, 'helvetica', 24,line,(x,y), col)
        y+=(size+2) 
  
def instruction(screen,buff):
    draw_string(screen,buff,(20,20),(255,255,255),20)
    
    
   
def next(buts,kk):
    
    return buts[2] or kk[pygame.K_q]



def write_wall(name,pts,fout):

    fout.write(name)
    count=0
    for pt in pts:
        if count > 0:
            fout.write(",")
            if count % 12 == 11 :
                fout.write("\n")
    
        fout.write(str(pt[0])+","+str(pt[1]))
        
        count+=1
    
    fout.write("\n")
    
init_surface(WINDOW_SIZE)


instruction(screen,"  Your track will be saved as \n \n   "+FILE_NAME+" \n\n\n  HITTING  ESCAPE AT ANY TIME WILL ABORT \n\n\n  press Q to continue")
blit(screen)


while True:
    
    if check_for_quit():
        sys.exit(0)

    buts,pos,kk=get_stuff()
    
    if next(buts,kk):
        pause()
        break
 

points=[]

redraw=True

while True:
    
    if check_for_quit():
        sys.exit(0)
    
    buts,pos,kk=get_stuff()
    
    if kk[pygame.K_d] and points:
        points.pop()
        redraw=True

    if next(buts,kk):
        pause()
        break
        
    if buts[0]:
        points.append(pos)
        redraw=True
        
    if redraw:
        clear_screen()
        draw_points(points,screen,False)
        instruction(screen,"Define left wall using left mouse button.    Q - when done.    D - delete last point")
        blit(screen)
        pause()
        redraw=False
            
    time.sleep(.05)   
             
pts2=[]

print points

for i in range(len(points)):
    ii=(i+1)%len(points)
    ptLast=points[ii-2]
    pt=points[ii-1]
    ptNext=points[ii]
    print ii,ptLast,pt,ptNext
    
    vec1=dir(ptLast,pt)
    vec2=dir(pt,ptNext)
    vec=add(vec1,vec2)

    ptNew=[int(pt[0]-(vec[1]*DEFAULT_WIDTH)/2),int(pt[1]+(vec[0]*DEFAULT_WIDTH)/2)]
    pts2.append(ptNew)
    

     
clear_screen()  
draw_trips(points,pts2,screen)
draw_points(points,screen,True)
draw_points(pts2,screen,True)
instruction(screen,"Drag points if you want to tweak it. Q when done.")
blit(screen)    


posLast=None
dragPt=None

pts=[]
pts.extend(points)
pts.extend(pts2)

while True:
    
    if check_for_quit():
        sys.exit(0)
    
    buts,pos,kk=get_stuff()
    
    if next(buts,kk):
        pause()
        break
        
    if buts[0]:
        if dragPt==None:
            dragPt=find_nearest(pts,pos)
        else:
            dragPt[:]=pos

        clear_screen()  
        draw_trips(points,pts2,screen)
        draw_points(points,screen,True)
        draw_points(pts2,screen,True)
        instruction(screen,"Drag points if you want to tweak it.    Q when done.")
        blit(screen)

    else:
        dragPt=None
    
    

podAng=math.pi*0.5

podPos=None

while True:
    
    buts,pos,kk=get_stuff()
       

    if check_for_quit():
        sys.exit(0)
    
    
    if buts[0]:
        podPos=pos
       
    if podPos: 
        d=dir(podPos,pos)
        if d != None:
            podAng=math.atan2(d[0],d[1])        
        if next(buts,kk):
            break
        
    clear_screen()  
  
    draw_points(points,screen,True)
    draw_points(pts2,screen,True)
    draw_trips(points,pts2,screen)
    if podPos:  
        draw_pod(podPos,podAng, screen,(255,0,0))
    else:
        draw_pod(pos,podAng, screen,(255,0,0))

    if not podPos: 
        instruction(screen,"Position CAR then press left button.")
    else:
        instruction(screen,"Angle CAR then press Q when done (this will save your track and exit).")
        
    blit(screen)
    
    

    
    

points.append(points[0])
pts2.append(pts2[0]) 
   
fout=open(FILE_NAME,"w")

write_wall("wall left\n",points,fout)
write_wall("\nwall right\n",pts2,fout)

fout.write("\npod\n")
buff="    "+str(podPos[0])+","+str(podPos[1])+","+ str(180.0*podAng/math.pi)
fout.write(buff+"\n")

       