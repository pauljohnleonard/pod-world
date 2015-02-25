


class YourController:

   
   def __init__(self):
       
       # something like
       self.network=Network() 
   
    # normal process called every time step    
    def process(self,pod,dt):
    
             
               
        # Decide if it is time to try another network
        # for example if the current car has crashed
        # The pod.sate should contain the information 
        # required to decide.
        #-------------------------------------------------
        # If so then 
        #    -calculate the fitness of the car
        #    (again use the information in pod.sate) 
        #  
        #    create a new candidate network 
        #
        
            
        # get the world to reset the pod to start of the track
             world.init_pod(pod)
             
            
        #  --- here if we normal control stuff
        
        control=pods.Control()

        # create the input form the pod state and sensor 
        # information. 
    
        output=network.fire(input)
        
        # assign control values using the output of the network
        
        return control



