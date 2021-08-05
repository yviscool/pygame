import turtle


turtle.speed(0)


for i in range(360):
    
    turtle.setheading(i)
    
    for i in range(8):
        turtle.forward(150)
        turtle.left(45)
