# make an empty list
x=[]

# add to the end

x.append(1.0)
x.append(2.0)

# list indices start with 0   (same as C and Java    NOT LIKE FORTRAN)
print x[0]

# or for the whole array
print x


# insert into the list (moves the other elements)

pos=1

x.insert(pos,3.0)

# x[pos] will now equal 3.0

print x

#  making a big empty array

size=10

x=size*[0]

x[3]=1

print x

# make a 2D array and fill with ones

size1=3
size2=4


# x=size1*[size2*[1]]     # !!!! DOES NOT WORK  (rows are all the same !!!!)
# see http://stackoverflow.com/questions/4230000/creating-a-2d-matrix-in-python
x=[size2*[1] for _ in range(size1)]

x[2][3]=4

print x

# make a 3D array 

size3=2

# Following the same pattern (best to disengage brain and just copy this!!!!)
x=[[size3*[3] for _ in range(size2)]  for _ in range(size1)]

# fill it with stuff

for i in range(size1):
    for j in range(size2):
        for k in range(size3):
            x[i][j][k]=k*100+j*10+i
print x


# some matrix operations

# 2 rows of 3 elements
a=[[1.,2.,3.],[4.,5.,6.]]
x=[1.,1.,1.]
c=[0.,0.]


# [a]*x

for row in range(len(a)):
    c[row]=0.0
    for col in range(len(x)):
        c[row]+=x[col]*a[row][col]

print c

