import turtle

t = turtle
t.speed(0)

t.bgcolor('black')

colors = ['red','purple','blue','green','orange', 'yellow']

for i in range(360):
    t.pencolor(colors[i%6])
    t.pensize(i/250 + 1)
    t.fd(i)
    t.left(59)
t.done()
