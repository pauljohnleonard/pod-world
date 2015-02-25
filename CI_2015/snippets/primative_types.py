
a = 1        # integer
b = 2.0      # floating number
c = True     # boolean
d = "Hello"  # a string


# take care with constants an expressions 

print " 1/2 = ",1/2     #   inteteger arithmetic result is 0

# it is very easy to do something like

x_array=[1,2,3,4]

z_array=[4,3,2,1]

print " Using integers "
for x,z in zip(x_array,z_array):
    print x/z


# make sure you use a decimal point if you want a float

x_array=[1.,2.,3.,4.]

z_array=[4.,3.,2.,1.]

print " Using floats "

for x,z in zip(x_array,z_array):
    print x/z
    
    
    
