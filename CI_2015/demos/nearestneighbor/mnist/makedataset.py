import numpy
import cPickle as pickle
import gzip
import random
  
# extract a subset of the data
     
# compressed data 
data_orig="mnist.pkl.gz"

# file to save data
data = "mnist_liteR1.pkl.gz"


f_orig=gzip.open(data_orig)
    
# load data into the 3 data sets
print " LOADING . . . . . ",
training_set,validation_set,test_set=pickle.load(f_orig)    
print " Making subset "

ntrain_orig=len(training_set[0])
ntest_orig=len(test_set[0])

ntrain=1000
ntest=200

train=[[],[]]
test=[[],[]]


random.seed()


for i in range(ntrain):
    ii=random.randint(0,ntrain_orig-1)
        
    train[0].append(training_set[0][ii])
    train[1].append(training_set[1][ii])


for i in range(ntest):
    ii=random.randint(0,ntest_orig-1)

    test[0].append(test_set[0][ii])
    test[1].append(test_set[1][ii])



f=gzip.open(data,"w")

pickle.dump((train,None,test),f)

f.close()

print " data written to: ",data
