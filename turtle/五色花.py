import turtle
a = 1
b = 1
c = 1
d = 1
e = 1
turtle.hideturtle()
turtle.speed(100000000000)
turtle.goto(0,0)
for i in range(200):
    turtle.pencolor('red')
    turtle.right(172)
    turtle.fd(b*25)
    b = b + 1
turtle.goto(0,0)
for i in range(200):
    turtle.pencolor('yellow')
    turtle.right(172)
    turtle.fd(c*25)
    c = c + 1
turtle.goto(0,0)
for i in range(200):
    turtle.pencolor('purple')
    turtle.right(172)
    turtle.fd(d*25)
    d = d + 1
turtle.goto(0,0)
for i in range(200):
    turtle.pencolor('green')
    turtle.right(172)
    turtle.fd(e*25)
    e = e + 1
turtle.goto(0,0)
for i in range(200):
    turtle.pencolor('blue')
    turtle.right(172)
    turtle.fd(a*25)
    a = a + 1
turtle.done()
