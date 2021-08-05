import turtle

t = turtle

t.bgcolor('black')
t.pencolor('white')

t.speed(0)
c = 0
d = 0

# for i in range(26):
# 	for i in range(4):
# 		t.fd(80)
# 		t.right(90)
# 	t.right(15)

# 12 连星星
# while True:
# 	for i in range(4):
# 		t.fd(80)
# 		t.right(90)
# 	t.right(15)
# 	c += 1
# 	if c >= 390/15:
# 		t.fd(50)
# 		c = 0
# 		d += 1
# 		if d >= 12:
# 			print('test')
# 			break

# 六连星星
while True:
	for i in range(4):
		t.fd(80)
		t.right(90)
	t.right(15)
	c += 1
	if c >= 420/15:
		t.fd(50)
		c = 0
		d += 1
		if d >= 6:
			print('test')
			break

t.done()
