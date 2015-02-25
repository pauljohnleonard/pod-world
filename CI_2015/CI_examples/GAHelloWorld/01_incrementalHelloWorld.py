"""
 Solve the HelloWorld problem by doing an incremental search.
 Keep best solution so far and nudge it till we find a better one.
"""

import random
import array
import copy

secret="Hello World!"
size=len(secret);

low_char=32
hi_char=121

           
def randomChar():
    return chr(random.randint(32,121))

def seed():
    string=array.array('c')
    for _ in xrange(size):
        string.append(randomChar())
    return string


def evaluate1(string):  # number correct
        summ=0
        for a,b in zip(string,secret):
            if a == b:
                summ += 1
        return summ
             
def mutate1(a):     # randomly replace a character
        i=random.randint(0,size-1)
        a[i]=randomChar()

    
def evaluate2(string):    #  sum of diff in char codes
        summ=0
        for a,b in zip(string,secret):
                summ -= abs(ord(a)-ord(b))
        return summ
        
def mutate2(a):    #  add/subtract 1 from the character code
        i=random.randint(0,size-1)
        ic = ord(a[i])
        im=random.randint(0,1)
        ic=ic + 2*im -1
        if ic >hi_char:
            ic=hi_char
        if ic <low_char:
            ic=low_char
        a[i]=chr(ic)
   
mutate=mutate1
evaluate=evaluate2

target_fitness=evaluate(secret)

cnt=0

max_eval=100000

string=seed()

best_str=string
best_fit=evaluate(string)

while cnt< max_eval:
    
    print cnt,": ",best_fit, best_str
   
    string=copy.deepcopy(best_str)
    mutate(string)
    
    fitness=evaluate(string)
    
    if fitness > best_fit:
        best_str=string
        best_fit=fitness
    
    cnt = cnt+1
    
    if fitness >= target_fitness:
        print "DONE IT"          
        print cnt,": ",best_fit, best_str  
        break
    
            
        