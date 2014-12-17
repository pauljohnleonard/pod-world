from math import *
import gui


class Admin:  # use me to control the simulation
              # see comments to see what key hits do
        
    def process(self,sim):   
        
            # this is called just before each time step
            # do admin tasks here
                          
            keyinput = gui.keys.key.get_pressed()
        
            # speed up/down  display      
            if keyinput[gui.keys.K_KP_PLUS] or keyinput[gui.keys.K_EQUALS]:
                sim.frameskipfactor = sim.frameskipfactor+1
                print "skip factor" ,sim.frameskipfactor
            
            if keyinput[gui.keys.K_MINUS]:
                sim.frameskipfactor = max(1,sim.frameskipfactor-1)
                print "skip factor" ,sim.frameskipfactor

class Simulation:
    """ The simulation class is responsible for running the Pod World.
     """

    def __init__(self,world,title,log_file=None):
        
        #: world     a World
        #: agents    list of agents
        
   
        self.admin=Admin()
        self.ticks=0
        self.slowMotionFactor=1.0
        self.world = world
        w,h=(self.world.dimensions())
        dim_world = (w+20,h+20)
        self.frameskipfactor=1
        self.frameskipcount=1
        self.painter=None
        
        self.screen = gui.init_surface(dim_world,title)
        
        if  log_file != None:
            self.log_file=open(log_file,"w")
            
        self.run_name=title
    
        
    def setPainter(self,painter):
        self.painter=painter
   
    def setAdmin(self,admin):
        self.admin=admin
   
            
    def run(self):
        """ start the simulation  
        """
        dt=self.world.dt
        clock = gui.clock()
        frameRate=1.0/dt/self.slowMotionFactor
        self.tick_count=0
        
        self.world.start()
         
            
        
       # the event loop also loops the animation code
        while True:
            
            self.frameskipcount -= 1
            self.tick_count += 1
            display= self.frameskipcount == 0 and self.frameskipfactor != 0

            if display:
                clock.tick(frameRate)
                self.frameskipcount=self.frameskipfactor

            if display or (self.tick_count%100)==0:
                gui.grab_events()
                if self.admin != None:
                    self.admin.process(self)
                  
            if gui.check_for_quit():
                break
            
            
            self.ticks += 1
            self.world.step()
            
            if display:
                self.screen.fill((0,0,0))
                
                if self.painter != None:
                    if self.painter.preDraw != None:
                        self.painter.preDraw(self.screen)
                    
                self.world.draw(self.screen)
                      
                
                if self.painter != None:
                    if self.painter.postDraw != None:
                        self.painter.postDraw(self.screen)
                gui.blit(self.screen)
                
                
