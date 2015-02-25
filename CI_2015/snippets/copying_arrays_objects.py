# be careful with lists, arrays and objects

a = [1,2,3,4]
b =a          # b and a refer to the same array/object

b[1]=42       # same as a[1]=42

print a       #   [1,42,3,4]

# if you want to copy an array or object use copy.deepcopy(object)

import copy

c = copy.deepcopy(b)

c[1]=0

print b      #   [1,42,3,4]