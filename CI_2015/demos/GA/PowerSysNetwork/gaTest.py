'''
Created on 29 Jun 2011

@author: pjl

Test the ga.py methods
'''
from ga import *


length=5
TOKRANGE=32
g1=random_gene(length,TOKRANGE)
g2=random_gene(length,TOKRANGE)

print " Parents "
print g1.str
print g2.str

print " Off springs "
for i in range(20):
    print mate(g1,g2).str

print " --Parent for mutate test ----------------"

b=blank_gene(length)

print b.str

print " Mutations ------------"
for i in range(20):
    mutate(b,TOKRANGE,1,0.5)
    print b.str