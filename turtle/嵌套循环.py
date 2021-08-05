import turtle

t = turtle
t.speed(5)

# t.bgcolor('black')
t.color('green')

for i in range(8):
    t.left(45)
    for j in range(8):
        t.fd(100)
        t.left(45)
