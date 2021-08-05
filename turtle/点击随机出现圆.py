import turtle
import random

t = turtle

t.speed(0)
t.hideturtle()
t.colormode(255)
def get_input(x, y):
	t.up()
	t.goto(x, y)
	t.down()
	t.dot(random.randint(0, 100), (
		random.randint(0, 255),
		random.randint(0, 255),
		random.randint(0, 255),
	))

turtle.onscreenclick(get_input)


turtle.done()
