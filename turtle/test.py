import turtle

t = turtle.Pen()
t1 = turtle.Pen()

t.speed(0)
t1.speed(0)

t.pencolor('black')
t1.pencolor('#CD5C5C')


for i in range(10000):
	t.forward(i)
	t1.forward(i)
	t.left(121)
	t1.right(121)


# turtle.speed(0)

# for i in range(10000):
# 	turtle.forward(i+5)
# 	turtle.left(121)

# turtle.dot(100)

# turtle.circle(200)

# turtle.done()



