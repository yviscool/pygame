from turtle import *
from random import *
from math import *
def tree(n, l):
    pd() 
    color("darkgoldenrod")
    pensize(n / 3)
    forward(l)
    if n > 0:
        b = random() * 15 + 10 
        c = random() * 15 + 10 
        d = l * (random() * 0.25 + 0.7) 
        right(b)
        tree(n - 1, d)
        left(b + c)
        tree(n - 1, d)
        right(c)
    else:
        right(90)
        color("gold")
        circle(3)
        left(90)
        if(random() > 0.7):
            pu()
            t = heading()
            an = -40 + random()*40
            setheading(an)
            dis = int(800*random()*0.5 + 400*random()*0.3 + 200*random()*0.2)
            forward(dis)
            setheading(t)
            pd()
            right(90)
            color("gold")
            circle(2)
            left(90)
            pu()
            t = heading()
            setheading(an)
            backward(dis)
            setheading(t)
    pu()
    backward(l)
ht() 
getscreen().tracer(800)
pu() 
backward(100)
left(90) 
pu() 
backward(300) 
tree(14, 100) 
done()
