import turtle

t = turtle

length = 0
angle = 0

t.bgcolor('black')
t.pencolor('green')

t.speed(0)

t.up()
t.goto(0, 200)
t.down()

t.ht()

while True:
	t.fd(length)
	t.right(angle)
	length += 3
	angle += 1
	if angle == 210:
		break

t.done()
