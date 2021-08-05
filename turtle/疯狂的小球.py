import pgzrun
import random

WEIGHT = 800
HEIGHT = 800



ball = []

for i in range(100):
    r = random.randint(10, 50)
    pos = [random.randint(100, 700), random.randint(100, 700)]
    c = [
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        ]
    speed_x = random.randint(1, 5)
    speed_y = random.randint(1, 5)
    speed = [
        speed_x,
        speed_y
    ]
    ball.append([
        pos,
        r,
        c,
        speed
    ])

def draw():
    screen.fill((255, 255, 255))
    for b in ball:
        pos = b[0]
        r = b[1]
        color = b[2]
        screen.draw.filled_circle(pos, r, color)

def update():
    for b in ball:

        pos = b[0]
        speed = b[3]

        x, y = pos
        speed_x, speed_y = speed

        x += speed_x
        y += speed_y

        if x > 800 or x < 0:
            speed_x *= -1
        if y > 800 or y < 0:
            speed_y *= -1

        b[0] = [x,y]
        b[3] = [speed_x, speed_y]



pgzrun.go()
