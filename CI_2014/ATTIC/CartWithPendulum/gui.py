"""
GUI routines  DO NOT EDIT
"""

import pygame

import math

import pygame
 
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
        Draw text with the given parameters on the given surface.
        
        surface - Surface to draw the text onto.
        
        fontName - Font name that identifies what font to use to draw the text.
        This font name must have been specified in the cFontManager 
        
        rectOrPosToDrawTo - Where to render the text at.  This can be a 2
        item tuple or a Rect.  If a position tuple is used, the align
        arguments will be ignored.
        
        color - Color to draw the text with.
        
        alignHoriz - Specifies horizontal alignment of the text in the
        rectOrPosToDrawTo Rect.  If rectOrPosToDrawTo is not a Rect, the
        alignment is ignored.
        
        alignVert - Specifies vertical alignment of the text in the
        rectOrPosToDrawTo Rect.  If rectOrPosToDrawTo is not a Rect, the
        alignment is ignored.
 
        antialias - Whether to draw the text anti-aliased or not.
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
 
def RunDemo():
    '''A simple demo of the use of the cFontManager class'''
    pygame.init()     
    pygame.display.set_mode((640, 480))
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
 
    # a font of None means to use the default font
  #  fontMgr = cFontManager((('Courier New', 16), (None, 48), ('arial', 24)))
    
    doQuit = False
    while not doQuit:
        clock.tick(60) # run at 60 fps
        screen.fill((0, 0, 0))
 
        white = (255, 255, 255)
        gray = (64, 64, 64)
        fontMgr.Draw(screen, 'Courier New', 16, 'Default font, 48', (0, 50), white)
        fontMgr.Draw(screen, None, 24, 'Default font, 24', (0, 0), white)
 
        rect = pygame.Rect(0, 100, 640, 60)
        pygame.draw.rect(screen, gray, rect)        
        # fontMgr.Draw(screen, 'arial', 24, 'Arial 24 top left', rect, white,
        #     'left', 'top')
        rect.top += 75
        
        pygame.draw.rect(screen, gray, rect)        
        # fontMgr.Draw(screen, 'arial', 24, 'Arial 24 centered', rect, white,
        #     'center', 'center')
        rect.top += 75
 
        pygame.draw.rect(screen, gray, rect)        
        # fontMgr.Draw(screen, 'arial', 24, 'Arial 24 bottom right', rect,
        #     white, 'right', 'bottom')
        rect.top += 75
 
        pygame.draw.rect(screen, gray, rect)        
        # fontMgr.Draw(screen, 'arial', 24, 'Arial 24 left center, anti-aliased',
        #     rect, white, 'left', 'center', True)
        rect.top += 75
        
        pygame.display.update()
        if pygame.QUIT in [event.type for event in pygame.event.get()]:
            doQuit = True
    pygame.quit()
    

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
     #   fontMgr = cFontManager((('Courier New', 12),('Courier New', 16), ('Courier New', 24), ('Courier New', 48)))
        return pygame.Surface(dim_world) #
 
def get_pressed():
    kk=pygame.key.get_pressed()
    return kk

def draw_string(screen,str1,point,col,size ):
    return
    fontMgr.Draw(screen, 'Courier New', size,str1,point, col) 


    
def clock():    
    return pygame.time.Clock() 


def tick(frameRate):
    clock().tick(frameRate)
    
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
    
