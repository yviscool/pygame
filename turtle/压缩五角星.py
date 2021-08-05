import turtle
turtle.colormode(255)
turtle.speed(0)
turtle.penup()
turtle.goto(-255,-125)
turtle.pendown()
j,k=0,255
for i in range(0,510):
    turtle.right(131)
    turtle.pencolor(i,j,k)
    turtle.forward(i-510)
    j+=1
    k-=1
    if j>255:
        j-=255
    if k<0:
        k+=255
