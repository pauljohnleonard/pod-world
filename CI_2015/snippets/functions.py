'''
Created on 1 Sep 2011

@author: pjl

A few function examnples.

'''

# this is how you define a function that returns a value

def add(a,b):
    return a+b

sum=add(4,5)
    
print sum

# you can return multiple values
def addsub(a,b):
    return a+b,a-b

sum,dif=addsub(4,5)
    
print sum,dif


# primitive arguments are copied
def change_me_not(z):
    z=6           # this z is a copy of x 
    
    
x=5  
change_me_not(x) 

print x     # prints 5   (not 6)


# you can use global values 
def you_can_see_globals():
    print x                 # global variables are visible
    
you_can_see_globals()



# by default you can not change global variables
def change_me_not2():
    x=6           # this creates a x within the function (yuck or what)
    
    
change_me_not2()
print x


# you can change global variables by declaring them global
def change_me():
    global x
    x=6           # now we refer to the global x
    
    
change_me()
print x

#  Objects and functions ....
class A:
    
    def __init__(self,val):
        self.val=val
        
        
a=A(10)


def you_can_change_an_objects_data(b):    # b is a reference (like a pointer)
    b.val=20
    
you_can_change_an_objects_data(a)

print a.val
    
    
    
    
    
    