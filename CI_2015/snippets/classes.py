

class A:


    def __init__(self,x):   #  constructor
        self.myx=x        # self is a reference to the object we are constructing


    def printx(self):     # all methods take self as first paramemter  (pointer to the object)
        print self.myx


a=A(5.0)    # make an instance of A

a.printx()  #  this will pass a reference to a into the self arg of printx


a.y=8.0     # python lets you add member data on the fly


print a.y

