import turtle as t
import random as rd

t.colormode(255)
t.pensize(1)
t.speed(10)
t.hideturtle()

t.penup()
t.goto(-320,240)
t.pendown()
t.color(255,255,255)
t.begin_fill()
t.forward(640)
t.right(90)
t.forward(480)
t.right(90)
t.forward(640)
t.right(90)
t.forward(480)
t.end_fill()

def flw(posX, posY, size, color):
    t.penup()
    t.goto(posX, posY)
    t.pendown()
    
    r = 255
    g = 255
    b = 255

    for i in range(250):
        if i%color == 0:
            g -= 1
            b -= 1
       
        t.pencolor(r, g, b)
        
        t.left(5)
        t.circle((250-i)/size, 50)

for j in range(20):
    flw(
        rd.randint(-200, 200),
        rd.randint(-200, 200),
        rd.randint(1,12),
        rd.randint(1,6)
    )



t.done()
