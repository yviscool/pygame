import  pgzrun



WIDTH=800
HEIGHT=700

inner_left_eye_x = 320
inner_right_eye_x = 480
inner_eye_y = 320

x = 0
y = 0

def draw():
    screen.fill((255, 255, 255))
    # 大脸
    screen.draw.filled_circle((400,400), 200, 'pink')
    # 左大眼
    screen.draw.filled_circle((320,320), 80, 'white')
    # 右大眼
    screen.draw.filled_circle((480,320), 80, 'white')

    # 鼻子
    screen.draw.filled_circle((400,400), 20, 'white')
    # 嘴巴
    screen.draw.filled_circle((400,500), 50, 'white')
    # 左眼珠
    screen.draw.filled_circle((inner_left_eye_x,inner_eye_y), 30, 'black')
    # 右眼珠
    screen.draw.filled_circle((inner_right_eye_x,inner_eye_y), 30, 'black')


# def update():
#     global inner_left_eye_x, inner_right_eye_x, inner_eye_y

#     if x < 320 and x > 0:
#         if 320/x < 10:
#             inner_left_eye_x =  320 - 320/ x * 5
#     elif x > 320 and x < WIDTH:
#         inner_left_eye_x = 320 +  x/320 * 20

#     if y > 320:
#         inner_eye_y =  320 + y/320 * 20
#     elif y < 320 and y >0:
#         if 320/y < 10:
#             inner_eye_y = 320 - 320/y *5

#     inner_right_eye_x = inner_left_eye_x + 160

def update():
    global inner_left_eye_x, inner_right_eye_x, inner_eye_y


    if x < 320 :
        inner_left_eye_x =  320 -  (1 - x/320) * 50
    else:
        inner_left_eye_x =  320 +  (1 - 320/x) * 80

    if y > 320:
        inner_eye_y =  320 + (1 - 320/y) * 80
    else:
        inner_eye_y =  320 - (1 - y/320) * 50

    inner_right_eye_x = inner_left_eye_x + 160

def on_mouse_move(pos):

    global x,  y
    x, y  = pos



pgzrun.go()
