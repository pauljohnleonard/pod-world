'''
Created on 28 Jun 2011

@author: pjl
'''


from math import *
import random
import gui

thresh=1
big_penalty=1e8



class World:
     
    # min token value required to build line
    maxTok=10

    def __init__(self,nGenerator=10,nConsumer=20):
        self.consumers=[]
        self.generators=[]
        self.lines=[]
       
        for i in range(nConsumer):
            demand=(0.4+random.random()*0.6)*Consumer.maxDemand
            x,y=gui.random_point();   
            self.consumers.append(Consumer(demand,x,y))
            
            
        for i in range(nGenerator):
            gen=(0.4+random.random()*0.6)*Generator.maxCapacity
            x,y=gui.random_point();
            self.generators.append(Generator(gen,x,y))
         
        for c in self.consumers:
            for g in self.generators:
                self.lines.append(Line(c,g))
        
        self.gene_length=nGenerator*nConsumer     
    
    def evaluate(self,gene,debug=False):   # number correct
        consumer_shortfall=0.0
        genrator_shortfall=0.0
        line_cost=0.0
        generator_cost=0.0
        
        
        cnt=0
        for c in self.consumers:
            for l in c.lines: 
                tok=gene.str[cnt]
                l.setToken(tok)
                cnt += 1

        for c in self.consumers:
            sup=c.supply()-c.demand
            if (sup < 0):
                consumer_shortfall -= sup
            
            line_cost += c.line_cost()
        
        for g in self.generators:
            demand = g.demand()
            if demand != 0:
                generator_cost += g.cost()
                sup=g.capacity-demand
                if sup < 0:
                    genrator_shortfall -= sup
            
        fitness=0.0

        if consumer_shortfall > 0:
            if debug:
                print "Consumer short fall ",consumer_shortfall   
            fitness -= (big_penalty + consumer_shortfall)
        
        if genrator_shortfall > 0:
            if debug:
                print "Generator short fall",genrator_shortfall    
            fitness -= (big_penalty+genrator_shortfall)
   
        if debug:
            print " line cost:",line_cost ,"  generator cost",generator_cost
            
            
        fitness -=  (generator_cost + line_cost)  
        
        return fitness
        
class Node:

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.lines=[]

        
class Generator(Node):
    
    costPerCapacity=100.0
    maxCapacity=100000.0
    
    def __init__(self,capacity,x,y):
        Node.__init__(self, x, y)
        self.capacity=capacity
        
    def demand(self):
        d=0.0
        for l in self.lines:
            d+=l.capacity 
        self.used =  (d > 0.0) 
        
        return d 
            
    def cost(self):
        if self.used:
            return self.capacity*Generator.costPerCapacity
        else:
            return 0.0
    

class Consumer(Node):
    
    # max power any consumer requires
    maxDemand=100.0
    
    def __init__(self,demand,x,y):
        Node.__init__(self, x, y)
        self.demand=demand

    def supply(self):
        sup=0
        for l in self.lines:
            sup+=l.capacity
        return sup
    
    def line_cost(self):
        c=0
        for l in self.lines:
            c += l.cost
        return c 
        
class Line:
    
    
    overhead=10000.0             # fixed cost for building any line
    costPerCapacity=100.0        
    maxCapacity=200.0
    
    def __init__(self,a,b):
        self.a=a;
        self.b=b;
        a.lines.append(self)
        b.lines.append(self)
        self.dist=sqrt((a.x-b.x)**2 +(a.y-b.y)**2)
        
    def setToken(self,tok):
        self.tok=tok
        if tok < thresh:
            self.capacity=0
            self.cost=0
        else:
            self.capacity=tok*Line.maxCapacity/World.maxTok
            self.cost=(Line.overhead+tok*Line.costPerCapacity)*self.dist

