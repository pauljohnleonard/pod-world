
# This code runs all the plugins in the folders in punters_test directory  using all the tracks in worlds_test
# The scores are written to results_test/results.txt
 
TIME_LIMIT=40.0      # Maximum time allowed for each attempt
TRIPS_LIMIT=60.0     # Goal in number of trip wires
GUI=True             # Switch GUI on /off
FPS_FACT=20           # Speed up factor
FONT_SIZE=16
USE_PREV_CONTROL=True

BASE_MARK=40.0
PJL_SCORE=336

import operator,importlib,traceback
from pod import simulation,pods,world
if GUI:
    from pod import gui,gui_base
    
import sys,os,imp,time,copy,pygame,datetime

print sys.argv

if len(sys.argv) > 1:
    punters=sys.argv[1:]
    print " Testing punters:",punters
else:
    punters=None


def inlist(name,exclude):
    for ex in exclude:
        if name == ex:
            return True
    return False

def all_punters(ex):
    list=os.listdir("punters_test")
    punters=[]
    for name in list:
        if not inlist(name,ex):
            punters.append(name)
                    
    return punters

def evaluate(pod):
   
    if pod.state.age > TIME_LIMIT:
        dist=pod.state.pos_trips-pod.state.neg_trips
        mess=" Time limit. Trips wires crossed ="+str(dist)
        score=dist
        pod.stat='T'
        return score,True,mess
    
    if pod.state.pos_trips - pod.state.neg_trips > TRIPS_LIMIT:
        mess=" Success age="+str(pod.state.age)
        score=TRIPS_LIMIT + (TIME_LIMIT-pod.state.age)  
        pod.stat='S'
        return score,True,mess
    
   

    if pod.state.collide:
        dist=pod.state.pos_trips-pod.state.neg_trips+pod.state.seg_pos
        age=pod.state.age
        mess=" Crashed age="+str(age)+" progress ="+str(dist)
        score=dist
        pod.stat='C'
        return score,True,mess
    
    dist=pod.state.pos_trips-pod.state.neg_trips
    score=dist
    pod.stat='R'
    return score,False,""

def tester(world_name,punter_names,fout):

    global simple_gui
    global FPS_FACT

    N=len(punter_names)
    
    
    ###  START OF PROGRAM
    world_test = world.World(world_name)



    pod_list=[]
    zombies=[]    
    cnt=0
    default_dir=os.getcwd()    
    
    for name in punter_names:
        pod   = pods.CarPod(world_test)
        pod_list.append(pod)
        pod.score=0.0
        pod.stat="-"
        pod.name=name
        pod.mess="Uninitialized"
        
        try:
            punters_path='punters_test/'+name
            os.chdir(punters_path)

            plug=importlib.import_module('punters_test.'+name+'.plugin')

            # call the plugin to equip the car 
            # set the current path to the punters directory
            plug.equip_car(pod)
            os.chdir(default_dir)
            
            pod.controller=plug.controller
            pod.control_state=pods.Control()

            hue=(360.0*cnt)/N
            col=pygame.Color(0)
            col.hsla=(hue,100,50,0)
            pod.col=(col.r,col.g,col.b)
            cnt+=1
        except:
            print name
            print "Unexpected error:", sys.exc_info()
#            fout.write(name+" Error "+ str(sys.exc_info()[0]))
            traceback.print_tb(sys.exc_info()[2])
            pod.mess="Loading Error: "+str(sys.exc_info()[0])
            pod.score=0.0
            pod.stat="E"
            zombies.append(pod)
            os.chdir(default_dir)
            
            
    runners=copy.copy(pod_list)

    # remove zombies      
    for pod in zombies:
        runners.remove(pod)
    
    if GUI:
        simple_gui=gui.SimpleGui(frames_per_sec=int(FPS_FACT/world_test.dt),world=world_test,pods=runners,back_ground=(5,5,5))
    
    
    # use a control to activate the car.
    control=pods.Control()
    
    while runners:
    
        zombies=[]
        
        for pod in runners:
            try:


                if USE_PREV_CONTROL:
                    control=pod.control_state
                else:
                    control.left=0
                    control.right=0
                    control.up=0
                    control.down=0

                pod.controller(pod,control)    
                pod.step(control)
                score,kill,mess=evaluate(pod)
                pod.score=max(score,0)
                pod.mess=mess
        
            except:
                   
                print name+": Unexpected error:", sys.exc_info()
                traceback.print_tb(sys.exc_info()[2])                
                pod.score=0
                pod.mess="RunError ->"+str(sys.exc_info())
                kill=True
                pod.stat="e"
                
            if kill:
                zombies.append(pod)
          
        # remove crashed      
        for pod in zombies:
            runners.remove(pod)

            
        ranked = sorted(pod_list, key = lambda x:x.score,reverse=True)
        
        
        if GUI:
            disp=""
            pos=[0,10]
            simple_gui.clear()
            
            for pod in ranked:
                col=pod.col
            
                gui_base.draw_string(simple_gui.screen,pod.stat+":"+pod.name,pos,col,FONT_SIZE,'Courier New') 
            
                pos[1]+=FONT_SIZE
                
            simple_gui.display(clear=False,fps=int(FPS_FACT/world_test.dt))
            
            if simple_gui.check_for_quit():
                sys.exit(0)
            
            if simple_gui.get_pressed()[gui.keys.K_p]:
                pause=True
                
            if simple_gui.get_pressed()[gui.keys.K_EQUALS]:
                FPS_FACT = min(FPS_FACT*2,200)
                print FPS_FACT
          
            if simple_gui.get_pressed()[gui.keys.K_MINUS]:
                FPS_FACT = max(int(FPS_FACT/2),1)
                print FPS_FACT
                 
                  
            if simple_gui.get_pressed()[gui.keys.K_s]:
                pause=False
            
            

    ranked=sorted(pod_list, key = lambda x:x.score,reverse=True)

    for pod in ranked:
        buff="%15s %6.3f %s" %   (pod.name+":",pod.score, ":"+pod.mess+"\n")
        fout.write(buff)
 
    return pod_list

def all_worlds(ex):
    list=os.listdir("worlds_test")
    worlds=[]
    for name in list:
        if not inlist(name,ex):
            worlds.append(name)
                    
    return worlds



d_str=time.strftime("%c")
print d_str


res_file="results_test/results_"+d_str+".txt"

#res_file="Results.txt"
fout=open(res_file,"w")


if punters==None:
    punter_names=all_punters([".svn","README.txt","__init__.py","__init__.pyc","__MACOSX"])
else:
    punter_names=punters


tot_score={}

for name in punter_names:
    tot_score[name]=0.0


world_names=all_worlds([".svn","README.txt"])   

for world_name in world_names:
    print "Doing:",world_name
    fout.write("WORLD:"+world_name+":------------------------------------------------------------------------------\n")
    pod_list=tester("worlds_test/"+world_name,punter_names,fout)         

    for pod in pod_list:
        tot_score[pod.name] += pod.score

    print "Done:",world_name

    dmy=raw_input(" CR to continue:")

results = sorted(tot_score.items(), key=operator.itemgetter(1))

fout.write(" Total scores (score) ***************************** \n")



sum=0.0
for line in results:
    sum += line[1]


for line in results:
    buff=" %10s : %6.2f " % (line[0],line[1])
    print buff
    fout.write(buff+"\n")


results = sorted(tot_score.items(), key=operator.itemgetter(0))

fout.write(" Total scores (names) ***************************** \n")

for line in results:
    buff=" %10s : %6.2f" % (line[0],line[1])
    print buff
    fout.write(buff+"\n")

print " EXITING "
fout.close()
sys.exit(0)
