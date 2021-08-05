import turtle

turtle.colormode(255)

r,g,b=10,240,240
rad=5

turtle.pensize(15)
#turtle.colormode(255)
turtle.speed(0)

turtle.bgcolor('black')

while(rad<100 and r<=255 and g>0 and b>0):
    turtle.pencolor(r,g,b)
    turtle.circle(rad,45)
    rad=rad+0.5
    r,g,b=r+1,g-1,b


