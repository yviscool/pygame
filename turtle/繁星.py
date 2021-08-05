
from turtle import *
from random import randint


def star(t, points, color, size, x_y):
    t.hideturtle()
    t.speed(0)

    t.penup()
    t.goto(x_y["x"], x_y["y"])
    t.pendown()

    colormode(255)
    t.color(color["red"], color["green"], color["blue"])
    t.begin_fill()

    angle = 180 - (180 / points)

    for s in range(points):
        t.forward(size)
        t.right(angle)

    t.end_fill()


for i in range(0, 500):
    bgcolor("black")
    pencil = Turtle()

    points = randint(2, 5) * 2 + 1
    colors = {"red": randint(0, 255),
              "green": randint(0, 255),
              "blue": randint(0, 255)}
    size = randint(10, 50)
    x_y = {"x": randint(-240, 240),
           "y": randint(-240, 240)}

    star(pencil, points, colors, size, x_y)

mainloop()
