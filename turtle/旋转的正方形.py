from turtle import *

speed(0)
bgcolor("white")
pencolor("MediumAquamarine")


h = 10

for j in range(360):

    for i in range(2):
        forward(h)
        right(90)

    right(3)
    h = h*1.01
