import robot
import math
import gui
import random
import sensFilters
import controller

def draw(screen,robot,pwmRatio):
    """
    Called by the simulation to display the current state of the robot.
    """ 
    #Get the robot state
    state = robot.getState()
    
    # Map robot angles to the screen coordinate system
    angW = (-state[0]) + math.pi    #Wheel angel
    angB = (angW + state[2])        #Body angle
    
    # Clear screen
    screen.fill((0,0,0))        
    
    # Gget the size of the window
    wid=gui.dim_window[0]
    hei=gui.dim_window[1]
    
    # Get robot dimensions
    length=robot.L
    scale = hei/length/3.0
    robot_r = int(robot.wR*1000)
    #robot_r = int(robot.wR*scale)    #Use this value for robot_r to display robot to scale
    
    # Robot position mapped to the screen coordinate system
    x1 = screen.get_width()/2                   #Robot reference X position on screen
    xm1 = (robot_r*state[0])%screen.get_width()  #Robot true X displacement on screen
    y1=hei*.6                                   #Robot base line for wheel on screen
    
    # X,Y Coordinate of the body's centre of gravity
    x2=x1+scale*math.sin(angB)*length
    y2=y1+scale*math.cos(angB)*length
    
    # Draw robot's centre of gravity
    col=(255,0,0)
    thick=3
    gui.draw_line(screen,x1,y1,x2,y2,col,thick)
    col=(0,255,0)
    gui.fill_circle(screen,x2,y2,6,col)
    
    # Draw wheel
    col=(0,0,255)
    gui.fill_circle(screen,x1,y1,robot_r,col)
    
    # Draw floor
    col=(255,255,0)
    thick=3
    gui.draw_line(screen,0,y1+robot_r,screen.get_width(),y1+robot_r,col,thick)
    
    # Draw floor reference lines
    col=(255,0,50)
    thick=8
    gui.draw_line(screen,screen.get_width()-xm1+x1,y1+robot_r,screen.get_width()-xm1+x1,y1+robot_r+40,col,thick)
    gui.draw_line(screen,screen.get_width()-xm1-x1,y1+robot_r,screen.get_width()-xm1-x1,y1+robot_r+40,col,thick)
    thick=3
    col=(255,255,255)
    gui.draw_line(screen,0.*screen.get_width()-xm1,y1+robot_r,0*screen.get_width()-xm1,y1+robot_r+20,col,thick)
    gui.draw_line(screen,0.25*screen.get_width()-xm1,y1+robot_r,0.25*screen.get_width()-xm1,y1+robot_r+20,col,thick)
    gui.draw_line(screen,0.75*screen.get_width()-xm1,y1+robot_r,0.75*screen.get_width()-xm1,y1+robot_r+20,col,thick)
    gui.draw_line(screen,1*screen.get_width()-xm1,y1+robot_r,1*screen.get_width()-xm1,y1+robot_r+20,col,thick)
    gui.draw_line(screen,1.25*screen.get_width()-xm1,y1+robot_r,1.25*screen.get_width()-xm1,y1+robot_r+20,col,thick)
    gui.draw_line(screen,1.75*screen.get_width()-xm1,y1+robot_r,1.75*screen.get_width()-xm1,y1+robot_r+20,col,thick)
    gui.draw_line(screen,2*screen.get_width()-xm1,y1+robot_r,2*screen.get_width()-xm1,y1+robot_r+20,col,thick)
            
    #Draw the wheel angle reference line    
    wx1 = robot_r*math.sin(angW)
    wy1 = robot_r*math.cos(angW)
    thick=3
    col=(255,255,255)
    gui.draw_line(screen,x1+wx1,y1+wy1,x1,y1,col,thick)
    
    # Display the state of the wheel and robot body
    str2=""
    str2+= "O: %5.2f "  % (state[0])
    str2+= "dO/dt: %5.2f " % (state[1])
    str2+= "beta: %5.2f "  % (state[2])
    str2+= "dbeta/dt: %5.2f " % (state[3])
    str2+= " pwmRatio: %5.2f " % (pwmRatio)        
    gui.draw_string(screen,str2,(20,10),col,16)
    
    # Copy the screen onto the display 
    gui.blit(screen)

""" MAIN CODE """

#Set GUI parameters and initialize screen
frameRate = 200   #Frames per second
screen = gui.init_surface((1200,800),"IP demo" )
      
# Create an instance of the robot, sensor filter and controller
robot = robot.Robot()
filter = sensFilters.CompFilter(robot)
controller = controller.Controller()

# Set the robot's initial tilt angle (rad) 
robot.setAngle(0.7)

while not gui.check_for_quit():   #  loop until user hits escape
    
    pwmRatio=0.0
    tau = 0.0
    
    #"""
    #TEST CONTROLLER OPERATION:
    state = robot.getState()
    phiFilt = filter.compFilter(1.0/frameRate,robot)
    sensors = robot.readSensors()
    pwmRatio = controller.PD(state[0],state[1],phiFilt,sensors[0])
    #"""
    
    #  Check for user key press
    keyinput = gui.get_pressed()
      
    if keyinput[gui.keys.K_LEFT]:    # apply anticlockwise pwmRatio to wheels
            tau = -0.8

    if keyinput[gui.keys.K_RIGHT]:   # apply clockwise pwmRatio to wheels
            tau = 0.8
            
    if keyinput[gui.keys.K_DOWN]:    # reset robot
            robot.setAngle(0.2*(random.random()-0.5))
    
    'CHANGE TO INPUT VOLTAGE in PWM format'
    
    # step the car for a single GUI frame        
    robot.step(pwmRatio,tau,1.0/frameRate)
    
    """
    ################  RESET CODE ##############################
    # Test for falling over
    # if fallen then reset with a random angle 
    
    if abs(robot.getPhi()) > math.pi/2: 
        robot.setAngle(0.2*(random.random()-0.5))
    ############################################################
    #"""   
    
    # draw the robot and display info
    draw(screen,robot,pwmRatio)
    
    # slow the gui down to the given frameRate
    gui.tick(frameRate)
    