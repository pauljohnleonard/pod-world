from math import *
import gui_base

keys=gui_base.keys

display_str=None
display_font_size=14

class SimpleGui:
    """ The simulation class is responsible for running the Pod World.
     """

    def __init__(self,world,pods,frames_per_sec,title="BraveNewWorld",back_ground=(0,0,0),log_file=None):
        
        #: world     a World
        #: agents    list of agents
        
        self.back_ground=back_ground
        self.pods=pods
        self.world = world
        if self.world != None:
            w,h=(self.world.dimensions())
        else:
            w,h=(1024-20 ,   768-20)
            
        dim_world = (w+20,h+20)
        
        self.screen = gui_base.init_surface(dim_world,title)
        
        if  log_file != None:
            self.log_file=open(log_file,"w")
            
        self.run_name=title
        self.frames_per_sec=frames_per_sec
        
        
    def check_for_quit(self):
        return gui_base.check_for_quit()
    
    def _display_mess(self,pos=(20,20),col=(255,255,0)):
        gui_base.draw_string(self.screen,display_str,pos,col,display_font_size)        
    
    def clear(self):
        self.screen.fill(self.back_ground)            
            
    def display(self,clear=True,fps=None):

               
        if clear:
            self.clear()
        
        if self.world==None:
            return
        
        self.world.draw(self.screen)
        for pod in self.pods:
            gui_base.draw_pod(pod,self.screen)
            gui_base.draw_sensors(pod,self.screen)
         
        if display_str!=None:
            self._display_mess()
            
        gui_base.blit(self.screen)
        if fps != None:
            self.frames_per_sec=fps
            
        if self.frames_per_sec > 0:
            gui_base.tick(self.frames_per_sec)
            
    def setWorld(self,world):
        self.world=world

        
    def get_pressed(self):
            return gui_base.get_pressed()
    
    def set_message(self,mess,font_size=12):
        global display_str,display_font_size
        display_str=mess
        display_font_size=font_size                
                
