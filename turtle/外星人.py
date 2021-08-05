import pgzrun
import random

alien = Actor('alien',)
alien.pos = 100, 56

print(alien.topright)
print(alien.left)
print(alien.right)
print(alien.top)
print(alien.bottom)
print(alien.width)
print(alien.pos)
# alien.topright = 0, 10

WIDTH = 200
HEIGHT = 200


def draw():
    screen.clear()
    alien.draw()

# def update():
    # alien.left += 2
    # if alien.left > WIDTH:
    #     alien.right = 0
    # alien.angle += 1

pgzrun.go()
