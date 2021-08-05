from turtle import *
from random import *
colormode(255)
speed(0)
goto(30,0)
a=0
r=0
for i in range(525):
    pencolor(225-i,225-2*i,500-i)
    circle(r,720)
    goto(30,a)
    a=a-1
    r=r+1
up()
for i in range(100):
    pensize(random())
    goto(randint(-600,300),randint(-250,300))
    pd()
    pencolor('white')
    for e in range(4):
        fd(3)
        bk(3)
        lt(90)
    up()
pensize(1)
goto(100,0)
for i in range(500,1000):
    pd()
    seth(233)
    if i>500:
        pencolor((i-500)*5/6,i-700,i*2/11-1)
    circle(i,70)
    lt(180)
    circle(-i,120)
    lt(180)
    circle(i,70)
    up()
    goto(i-400,0)
up()
home()
goto(-200,0)
pd()
seth(0)
pensize(0.5)
st()
pencolor('black')
def t(a,s):
    b=(int(random())+10)*3
    c=int(random())*50
    d=int(random())*20
    if a > 3:
        fd(a)
        rt(s)
        bk(a)
        t(a-10,s)
        fd(a)
        lt(2*s)
        t(a-10,s)
        rt(s)
    bk(a)
pensize(0.35)
penup()
sety(-50)
pendown()
backward(100)
t(100,20)
fillcolor('white')
color('white')
stamp()
up()
goto(80,-23)
pencolor('white')
ht()
pd()
seth(233)
for i in range(4):
    fd(3)
    bk(3)
    lt(90)
done()
