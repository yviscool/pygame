import turtle

t = turtle.Turtle()
t.hideturtle()
FillColors=[
    '#FFFFFF',
    '#8B0000',
    '#B22222',
    '#A52A2A',
    '#8B2323',
    '#CD3333'
]


def get_midpoint(a, b):
    ax, ay = a
    bx, by = b
    return (ax + bx) // 2, (ay + by) // 2


def draw_triangle(a, b, c, depth):
    ax, ay = a
    bx, by = b
    cx, cy = c
    
    t.penup()
    _tcolor = FillColors[depth % len(FillColors)]

    t.color("white", _tcolor)
    t.goto(ax, ay)
    t.pendown()
    t.begin_fill()
    t.goto(bx, by)
    t.goto(cx, cy)
    t.goto(ax, ay)
    t.end_fill()
    t.penup()


def draw_sierpinski(triangle, depth):
    a, b, c = triangle
    draw_triangle(a, b, c, depth)
    if depth == 0:
        return
    else:
        d = get_midpoint(a, b)
        e = get_midpoint(b, c)
        f = get_midpoint(c, a)
        draw_sierpinski([a, d, f], depth-1)
        draw_sierpinski([d, b, e], depth-1)
        draw_sierpinski([f, e, c], depth-1)


if __name__ == '__main__':
    triangle = [[-300, -200], [0, 300], [300, -200]]
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(-300,300)
    turtle.pendown()
    turtle.begin_fill()
    turtle.color("white")
    for i in range(2):
        turtle.fd(600)
        turtle.right(90)
        turtle.fd(600)
        turtle.right(90)
    turtle.end_fill()
    draw_sierpinski(triangle, 5)
    turtle.done()

