"""
Program to display data from the MNIST data base
"""

import os, sys
import Tkinter
import Image, ImageTk
import gzip
import cPickle
from numpy import *
import PIL.Image

# get an image from the data set according to the given index
# requires Pythin Imaging Library

def grabImage(index,set):
    # print set[0][index]
    x=reshape(set[0][index],(28,28))
    x=x*256.0
    image=PIL.Image.fromarray(x)
    return image


#  exit application

def button_click_exit_mainloop (event):
    event.widget.quit() # this will cause mainloop to unblock.

# compressed data
data="mnist_lite.pkl.gz"

f=gzip.open(data)

# load data into the 3 data sets
print " LOADING .....",
training_set,validation_set,test_set=cPickle.load(f)    
print " DONE"


# Root of the gui
root = Tkinter.Tk()


tkpimages=[]



set=test_set
iw=28
ih=28
nRow=50
nPerRow=20
# root.geometry('%dx%d' % (iw*N,ih))
N=min(len(set[0]),nRow*nPerRow)

img=[]
for i in range(N):
    image1 = grabImage(i,set)          
    # tkpimages.append(ImageTk.PhotoImage(image1))
    img.append(ImageTk.PhotoImage(image1))
    label_image = Tkinter.Label(root,image=img[i])  # tkpimages[i])
    label_numb=Tkinter.Label(root,text=str(set[1][i]))
    
    col=(i%nPerRow)*2
    row=int(i/nPerRow)
    label_image.grid(row=row,column=col+1)
    label_numb.grid(row=row,column=col)


root.title(f)
root.mainloop() # wait until user clicks the window
 