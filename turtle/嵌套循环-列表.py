import turtle

t = turtle
t.speed(0)
t.bgcolor('black')

colors = ['red', 'magenta','blue','cyan','green','yellow']

# # 一
# for color in colors:
#     t.color(color)
#     t.left(12)
#     for i in range(4):
#         t.fd(200)
#         t.left(90)
for i in range(int(360/12)):
    t.color(colors[i%len(colors)])
    t.left(12)
    for i in range(4):
        t.fd(200)
        t.left(90)

# for x in range(10):

#     for color in colors:

#         t.color(color)
#         t.left(360/10/len(colors))

#         for i in range(4):
#             t.fd(200)
#             t.left(90)

t.done()
