import turtle as tt
from random import randint
tt.speed(0)  # 绘图速度为最快
tt.bgcolor("black")  # 背景色为黑色
tt.setpos(-25, 25)  # 改变初始位置，这可以让图案居中
tt.colormode(255)
cnt = 0
r=255
g=255
b=255
while cnt < 300:
    if(r>0):
            r-=1
    if(r==0 and g>0):
            g-=1
    if(r==0 and g==0):
            b-=1
    tt.pencolor(r, g, b)  # 画笔颜色每次随机
    print(r, g, b)
    tt.forward(5 + cnt)
    tt.right(61)
    cnt += 0.3
