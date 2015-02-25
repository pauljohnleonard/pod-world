'''
Knearest is a class to help implement the k-nearest scheme.

A simple main program shows how to usxe this class 

Usage:

To test a vector  (test point) 

import knearest

k=    value of k for the scheme
kn=knearest.Knearest(k) 

#We calculate the distance between the test point and
#each point of known classifications.
#We feed the KNearest object this data.
#It maintains a record of the k nearest points and their classification

for all training data points:
   
      # do the distance from test to training point here
      # add data to kn
      kn.add(distance_to_training_point,classification_of_training_point)


#After doing this we can ask the Knearest object which class gets the most votes

test_classification=kn.get_knearest()  

'''




class Knearest:
    
    BIG=1e32                 # bigger than any distance we are likely to encounter
               
    def __init__(self,k):
        
        # initialise the table with NULL entries
        # this means we don't have special cases whilst filling up the table.
        
        self.min_table=k*[(Knearest.BIG,-1)]   # table of    [distance,output]   pairs 
        self.k=k
        
# add a single pair if distance is less than any already stored
    def add(self,dist,out):
        if dist > self.min_table[self.k-1][0]:
            return
        
        for i in range(self.k):         # go through the table
            if dist < self.min_table[i][0]:              # if distance less than a value already stored
                self.min_table.insert(i,[dist,out])      # insert new pair
                self.min_table.pop()                     # discard the last entry to keep list size equal to k
                return

    
    def debug(self):
        print " DEBUG --------------- "
        for i in range(self.k):
            print self.min_table[i][0], self.min_table[i][1]

    def get_knearest(self):     
        # Now construct a dictionary that contains the number occurances of any output
        dict={}     #    output  ->  no of occurances
        for i in range(self.k):                   # iterate on the minimum table
                out=self.min_table[i][1]          
                count=dict.get(out)           
                if count == None:           # if this output  is not in dictionary
                    dict[out]=1             # add an entry with count of 1
                else:
                    dict[out]=dict[out]+1   # otherwise increment the count
        # Now look in the dictionary to find the  output that occurs the most times
        max_occurances=0
        knearest=None
        
        for out in dict:
            if dict[out] > max_occurances:
                max_occurances=dict[out]
                knearest=out
        
        return knearest


# Test example
def test():
    # test data pairs of distances and values in parallel arrays
    dists = [4,5,2,1,6,7,8,9,1,20]
    outs  = [1,0,2,3,4,0,2,5,2,4]
    
    k=9                     # number of nearest to look at            
    
    knearest=Knearest(k)     # create a Knearest object
    
    # loop on data pairs and construct the minimal distance table
    for i in range(len(dists)):
            knearest.add(dists[i],outs[i])
          #  knearest.debug()  
            
            
    print knearest.get_knearest()

    
if __name__ == "__main__":
    test()
    


            

