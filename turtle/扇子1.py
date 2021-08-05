import turtle
a=turtle.Pen()
a.left(15)
a.speed(0)
for i in range(500):
    a.pencolor('red')
    a.forward(300)
    a.pencolor('black')
    a.backward(350)
    a.forward(50)
    a.left(150/500)
turtle.done()
