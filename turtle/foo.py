# 导入海龟
import  turtle
import  time

turtle.hideturtle()

turtle.fillcolor('black')
turtle.begin_fill()
turtle.fd(100)
turtle.left(90)
turtle.fd(300)
turtle.left(90)
turtle.fd(100)
turtle.left(90)
turtle.fd(300)
turtle.end_fill()

turtle.up()
turtle.goto(50, 250)
turtle.down()
turtle.dot(50, 'red')

time.sleep(1)

turtle.up()
turtle.goto(50, 180)
turtle.down()
turtle.dot(50, 'green')

time.sleep(1)
turtle.up()
turtle.goto(50, 100)
turtle.down()
turtle.dot(50, 'yellow')

turtle.up()
turtle.goto(0, -100)
turtle.down()

turtle.write("红灯停, 绿灯行", align="left", font=("微软雅黑", 50,"bold"))

turtle.done()
