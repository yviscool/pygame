#!/usr/bin/env python3

from turtle import *
from datetime import *

def Skip(step):
    penup()
    forward(step)
    pendown()

def Setupclock(radius):
    # 建立一个表的框格
    # 初始化
    reset()
    # 笔的大小
    pensize(7)
    # 每隔五格画一长的
    for i in range(60):
        Skip(radius)
        if i % 5 == 0:
            color('purple')
            forward(20)
            color('black')
            Skip(-radius - 20)
        else:
            dot(5)
            Skip(-radius)
        right(6)

def mkHand(name,length):
    reset()
    Skip(-length*0.1)
    #begin_poly()画图
    #end_poly()
    #get_poly()
    #-->得到图形
    begin_poly()
    forward(length*1.1)
    end_poly()
    handForm = get_poly()
    register_shape(name,handForm)

def Init():
    global sHand, mHand, hHand, printer  # 全局变量
    #mode('logo')  # 画笔改为向北，顺时针
    #color('red')
    mkHand('sHand',125)
    #color('black')
    mkHand('mHand', 130)
    mkHand('hHand', 90)
    # Turtle是turtle模块中的一个类，这样将三个表针实例化
    # 建立秒针对象，shape是Turtle类中的方法
    sHand = Turtle()
    sHand.shape('sHand')
    mHand = Turtle()
    mHand.shape('mHand')
    hHand = Turtle()
    hHand.shape('hHand')
    for hand in sHand, mHand, hHand:
        hand.shapesize(1, 1, 3)
        hand.speed(0)  # 速度最快，设为其他数时，有一个变化过程。
        # 建立输出文字Turtle
    printer = Turtle()  # 同样实例化，将输出文字为类的一个对象
    printer.hideturtle()
    printer.penup()

def Week(t):
    week = ["星期一", "星期二", "星期三","星期四", "星期五", "星期六", "星期日"]
    return week[t.weekday()]

def Date(t):
    y = t.year
    m = t.month
    d = t.day
    return '%s.%d.%d' % (y,m,d)

def Tick():
    t = datetime.today()
    second = t.second + t.microsecond*0.000001
    minute = t.minute + second/60.0
    hour = t.hour + minute/60.0
    sHand.color('red')
    sHand.setheading(180-6*second)
    mHand.setheading(180-6*minute)
    hHand.setheading(180-30*hour)



def main():
    # 执行作图代码时，窗口并不会出现任何东西，
    # 应该是保持开始作图之前的画面，直到执行tracer(True)刷新画面。
    #tracer(n=None,delay=None)设置动画开关和延迟
    #update()更新屏幕
    #ontimer(fun, t=0)每隔时间运行
    #tracer(False)
    Init()
    Setupclock(160)
    #tracer(True)
    hideturtle()
    for i in range(100000):
        Tick()
    
    mainloop()

if __name__ == "__main__":
    main()





























