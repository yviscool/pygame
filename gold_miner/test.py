import pygame
import random
import math
from pygame import mixer
from pygame.sprite import Sprite

mixer.init()
pygame.init()

# 首先窗口大小
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gold Miner')

# 设置游戏帧数
clock = pygame.time.Clock()
FPS = 60

# 播放背景音乐
pygame.mixer.music.load('mining_music.wav')
# pygame.mixer.music.load('bg.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

# 场景
# 0 正在启动
# 1 游戏规则
# 2 开始游戏
# 3 商店
# 4 游戏
scene = 0
# 当前 level
level = 1
# level 对应的分数
money_goal=[1000,2200,3600,5400,7500,10000,12500,17000,21500,26000,30000,45000]
# 玩家金钱
money=0
# 摆动的角度 从 -70 到 70
degree = -70
# 绳子长度
chain_distance = 30
# 绳子增加速度
speed = 5
# 物品拉回来的时候停留时间
popped_up_word_counterdown = 16
# 绳子摆动方向
direction_left_to_right=True
# 拉扯物体的重量
weight_item_caught = speed + 5
# 抓取物品的价值
value_caught = 0

# 倒计时
counter = 0
# 倒计时毫秒数
counter_time = None


item_lamp = False
item_time = False
item_luck = False
item_rocks = False

# 绳子去 按下下键出发
chain_thrown_out = False
# 控制绳子来去  去 True  回 False
chain_thrown_out_away = True
# 绳子碰到黄金等物品
chain_thrown_out_catchsomething = False


gold_middle = pygame.sprite.Group()
gold_small = pygame.sprite.Group()
gold_large = pygame.sprite.Group()
gold_diamond = pygame.sprite.Group()
gold_small_rock = pygame.sprite.Group()
gold_big_rock = pygame.sprite.Group()
gold_random_big = pygame.sprite.Group()
catch_gold_group = pygame.sprite.Group()

# 字体
yahei_font40 = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 40)
yahei_font30 = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 30)
yahei_font20 = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 20)


# 绘制文本
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# 缩放图片
def scale_img(img, scale):
    w = img.get_width()
    h = img.get_height()
    img = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
    return img

picture_list=[
    "picture/gold_small.png",
    "picture/gold_middle.png",
    "picture/gold_big.png",
    "picture/rock_small.png",
    "picture/rock_big.png",
    "picture/dimaond.png",
    "picture/mystery_bag.png",
    "picture/background.png",
    "picture/background2.png",
    "picture/machine.png",
    # "picture/Starting screen.png",
    "picture/starting_screen.png",
    "picture/shop.png",
    "picture/intro.png",
    'picture/restart_btn.png',
]

item_picture_list = [
    "picture/gold samd.png",
    "picture/polisher.png",
    "picture/lamp.png",
    "picture/red gem.png",
    "picture/purple gem.png",
    "picture/green gem.png",
    "picture/lucky rock.png"
]

# load image
# bg
start_bg_img = pygame.image.load(picture_list[10]).convert_alpha()
# start_bg_img = scale_img(start_bg_img, 0.7)

body_img = pygame.image.load(picture_list[7]).convert_alpha()
body_img = scale_img(body_img, 0.7)

head_img = pygame.image.load(picture_list[8]).convert_alpha()
head_img = scale_img(head_img, 0.45)

machine_img = pygame.image.load(picture_list[9]).convert_alpha()
machine_img = scale_img(machine_img, 0.2)


# 小黄金
gold_small_img = pygame.image.load(picture_list[0]).convert_alpha()
# 中黄金
gold_middle_img = pygame.image.load(picture_list[1]).convert_alpha()
# 大黄金
gold_big_img  = pygame.image.load(picture_list[2]).convert_alpha()
# 小石头
rock_small_img = pygame.image.load(picture_list[3]).convert_alpha()
# 大石头
rock_big_img = pygame.image.load(picture_list[4]).convert_alpha()
# 钻石
diamond_img = pygame.image.load(picture_list[5]).convert_alpha()
# 神秘背包
mystery_bag_img = pygame.image.load(picture_list[6]).convert_alpha()

item_boxes = {
    'gold_small' : gold_small_img,
    'gold_middle'   : gold_middle_img,
    'gold_big': gold_big_img,
    'rock_small': rock_small_img,
    'rock_big': rock_big_img,
    'diamond': diamond_img,
    'mystery_bag': mystery_bag_img,
}

# 角色
class Character(Sprite):

    def __init__(self, x, y):

        Sprite.__init__(self)

        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        sheet_idle = pygame.image.load('picture/character1_1.png')

        width = sheet_idle.get_width() / 7
        height = sheet_idle.get_height() / 1

        for row in range(1):
            temp_list = []
            for col in range(7):
                clip = pygame.Rect(
                    col * width,
                    row * height,
                    width,
                    height
                )
                frame = sheet_idle.subsurface(clip)
                # w = frame.get_width()
                # h = frame.get_height()
                # frame = pygame.transform.smoothscale(frame, (int(w* 0.5), int(h* 0.5)))
                temp_list.append(frame)
            self.animation_list.append(temp_list)

        sheet_pull = pygame.image.load('picture/character1_2.png')

        width = sheet_pull.get_width() / 8
        height = sheet_pull.get_height() / 1

        for row in range(1):
            temp_list = []
            for col in range(8):
                clip = pygame.Rect(
                    col * width,
                    row * height,
                    width,
                    height
                )
                frame = sheet_pull.subsurface(clip)
                # w = frame.get_width()
                # h = frame.get_height()
                # frame = pygame.transform.smoothscale(frame, (int(w* 0.5), int(h* 0.5)))
                temp_list.append(frame)
            self.animation_list.append(temp_list)


        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):

        ANIMATION_COOLDOWN = 80

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


# 轮子/绳子的头部
class Chainhead(Sprite):

    def __init__(self, x, y):

        Sprite.__init__(self)

        self.animation_list = []
        self.animation_dict = {}
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.pick_type = None

        # sheet = pygame.image.load('picture/hook.png')
        sheet = pygame.image.load('picture/animation1.png')

        width = sheet.get_width() / 7
        height = sheet.get_height() / 1

        for row in range(1):
            for col in range(7):
                clip = pygame.Rect(
                    col * width,
                    row * height,
                    width,
                    height
                )
                frame = sheet.subsurface(clip)
                w = frame.get_width()
                h = frame.get_height()
                frame = pygame.transform.smoothscale(frame, (int(w* 0.5), int(h* 0.5)))
                self.animation_list.append(frame)

        self.image = self.animation_list[self.frame_index]
        # w = sheet.get_width()
        # h = sheet.get_height()
        # self.image = pygame.transform.scale(sheet, (int(w* 0.08), int(h* 0.08)))

        # angle = -70
        # while angle < 80:
        #     img = pygame.transform.rotate(self.image, angle)
        #     self.animation_dict[angle] = img
        #     angle += 1.5
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):

        global chain_thrown_out_away, weight_item_caught, speed, value_caught, chain_thrown_out_catchsomething

        if chain_thrown_out_catchsomething == False:

            if pygame.sprite.spritecollide(self, gold_middle, True):
                chain_thrown_out_away = False
                chain_thrown_out_catchsomething = True
                weight_item_caught = speed - 3
                value_caught = 200
                self.pick_type = 'gold_middle'

            if pygame.sprite.spritecollide(self, gold_small, True):
                chain_thrown_out_away = False
                chain_thrown_out_catchsomething = True
                weight_item_caught = speed - 1
                value_caught = 75
                self.pick_type = 'gold_small'

            if pygame.sprite.spritecollide(self, gold_large, True):
                chain_thrown_out_away = False
                chain_thrown_out_catchsomething = True
                weight_item_caught = speed - 5
                value_caught = 500
                self.pick_type = 'gold_big'

            if pygame.sprite.spritecollide(self, gold_diamond, True):
                chain_thrown_out_away = False
                chain_thrown_out_catchsomething = True
                weight_item_caught = speed + 4
                value_caught = 600 + 50 * level
                self.pick_type = 'diamond'

            if pygame.sprite.spritecollide(self, gold_small_rock, True):
                chain_thrown_out_away = False
                chain_thrown_out_catchsomething = True
                weight_item_caught = speed - 3
                value_caught = 20
                self.pick_type = 'rock_small'

            if pygame.sprite.spritecollide(self, gold_big_rock, True):
                chain_thrown_out_away = False
                chain_thrown_out_catchsomething = True
                weight_item_caught = speed - 4
                value_caught = 60
                self.pick_type = 'rock_big'

            if pygame.sprite.spritecollide(self, gold_random_big, True):
                chain_thrown_out_away = False
                chain_thrown_out_catchsomething = True
                weight_item_caught = speed + random.randint(-4, 5)
                value_caught = random.randint(-300, 700)
                self.pick_type = 'mystery_bag'


        if chain_thrown_out_catchsomething:
            if self.pick_type:
                item = Gold(
                    self.pick_type,
                    500 + math.sin(math.radians(degree)) * 2.5 * (chain_distance+10),
                    75 + math.cos(math.radians(degree)) * 2.5 * (chain_distance+10),
                    True,
                )
                catch_gold_group.add(item)
                self.pick_type = None

        self.update_animation()


    def update_animation(self):

        ANIMATION_COOLDOWN = 30

        self.image = self.animation_list[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

        # self.image = self.animation_dict.get(degree, self.image)


# 轮子
class Gold(Sprite):

    def __init__(self, type, x, y, move = False):

        Sprite.__init__(self)


        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.move = move

        self.image = item_boxes[type]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    # 重叠
    def touches(self, other):

        return pygame.sprite.collide_rect(self, other)

    def update(self):

        # 当绳子碰到黄金时候, 删除 group 里面的黄金, 同时生成对应的黄金, 跟着移动
        if self.move:

            pos = (
                500 + math.sin(math.radians(degree))  * 2.5 * (chain_distance+10),
                75 + math.cos(math.radians(degree))  * 2.5 * (chain_distance+10),
            )

            self.rect.center = pos

            # 当不需要拉扯的时候 删除该黄金
            if chain_thrown_out_catchsomething == False:
                self.kill()

# 雷管爆炸效果
class Boom(Sprite):

    def __init__(self, x, y):

        Sprite.__init__(self)

        self.animation_list = []
        self.frame_index = 0

        sheet = pygame.image.load('picture/boom.png')

        width = sheet.get_width() / 8
        height = sheet.get_height() / 1

        for row in range(1):
            for col in range(8):
                clip = pygame.Rect(
                    col * width,
                    row * height,
                    width,
                    height
                )
                frame = sheet.subsurface(clip)
                w = frame.get_width()
                h = frame.get_height()
                frame = pygame.transform.smoothscale(frame, (int(w* 0.5), int(h* 0.5)))
                self.animation_list.append(frame)

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):


        if self.frame_index < len(self.animation_list) -1 :
            self.frame_index += 1
            self.image = self.animation_list[self.frame_index]

        # 结束动画后 删除
        if self.frame_index >= len(self.animation_list) -1:
            self.kill()

#button class
class Button():

    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):

        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


# 显示 当前关卡目标分数, 当前金额, 剩余时间等信息
def show_info():

    global value_caught

    draw_text(f'关卡:{level} 目标分数: {money_goal[level-1]}' , yahei_font30, 'white', 650, 85)
    draw_text(f'当前金额: {money}' , yahei_font20, 'yellow', 60, 18)
    draw_text(f'剩余时间: {counter}' , yahei_font20, 'black', 60, 44)


    # 当抓到物品到达目标点的时候 value_caught !=0 , popped_up_word_counterdown 从 1 开始增加,
    if popped_up_word_counterdown <= 15:
        if value_caught > 0:
            draw_text(f'+{value_caught}' , yahei_font30, 'green', 270, 20)
        else:
            draw_text(f'-{value_caught}' , yahei_font30, 'red', 270, 20)
    # 金钱显示 popped_up_word_counterdown 1-15 时候, 重置抓取物品价格
    elif popped_up_word_counterdown == 16:
        value_caught = 0


# 倒计时
def countdown():

    global counter, counter_time, scene, level

    one_second = 1000

    if counter == 0:

        if money < money_goal[level - 1]:
            scene = 4
            return None
        else:
            level += 1
            if level > 12:
                level = 0
            level_generation(level)

    if pygame.time.get_ticks() - counter_time > one_second:
        counter_time = pygame.time.get_ticks()
        counter -= 1



# 生成关卡
def level_generation(level):

    global counter, counter_time, gold_small_rock ,gold_large, gold_middle, gold_small, gold_random_big, gold_diamond, gold_big_rock
    # 小黄金
    gold_small.empty()
    # 中黄金
    gold_middle.empty()
    # 大黄金
    gold_large.empty()
    # 钻石
    gold_diamond.empty()
    # 小石头
    gold_small_rock.empty()
    # 大石头
    gold_big_rock.empty()
    #   随机
    gold_random_big.empty()

    # item evaluation
    if item_time == True:
        counter = 80
    else:
        counter = 60

    counter_time = pygame.time.get_ticks()

    if item_lamp == True:
        no_diamond = 3
    else:
        no_diamond = 0

    # generative algorithm
    if level % 4 == 0:
        no_diamond += 2
        no_diamond += int(level/3)
    if level % 2 == 0:
        no_random = 3
        no_random += int(level/2)
    else:
        no_random = 1
    if level >= 3:
        no_big = 1
        no_big += level//2
    else:
        no_big = 0
    if level >= 6:
        no_diamond += 2
        no_big += 2
        no_random += 2
        base = 1
    else:
        base = 0

    if level >= 8:
        no_diamond += 4
        no_big += 3
        no_random += 3
        base = 2
    if level == 12:
        no_diamond += 10
        base = 5
        no_big = 6
        no_random = 6

    # 生成小黄金
    for c in range(0, random.randint(5 + level // 2, 12 + level // 2)):
        item = Gold(
            'gold_small',
            random.randint(50, 950),
            random.randint(200, 690),
        )
        gold_small.add(item)

    # 生成小石头
    for c in range(0, random.randint(5, 7)):
        # 判断小石头和小黄金以及小石头重叠
        touched = True
        while touched:
            item = Gold(
                'rock_small',
                random.randint(50, 950),
                random.randint(200, 690),
            )

            touched = False

            for i in gold_small:

                if item.touches(i):
                    touched = True

            for i in gold_small_rock:

                if item.touches(i):
                    touched = True


        gold_small_rock.add(item)


    # 生成中黄金
    for c in range(0, random.randint(5+level//2, 8+level//2)):
        # 判断中黄金和小黄金,小石头以及中黄金重叠
        touched = True
        while touched:
            item = Gold(
                'gold_middle',
                random.randint(50, 950),
                random.randint(200, 690),
            )

            touched = False

            for i in gold_small:
                if item.touches(i):
                    touched = True
            for i in gold_small_rock:
                if item.touches(i):
                    touched = True
            for i in gold_middle:
                if item.touches(i):
                    touched = True

        gold_middle.add(item)


    # 生成大石头
    for c in range(0, random.randint(1+level//4+base, 3+level//4+base)):
        touched = True
        while touched:
            item = Gold(
                'rock_big',
                random.randint(50, 950),
                random.randint(200, 690),
            )

            touched = False

            for i in gold_small:
                if item.touches(i):
                    touched = True
            for i in gold_small_rock:
                if item.touches(i):
                    touched = True
            for i in gold_middle:
                if item.touches(i):
                    touched = True
            for i in gold_big_rock:
                if item.touches(i):
                    touched = True

        gold_big_rock.add(item)


    # 生成大黄金
    for c in range(0, random.randint(base, no_big)):
        touched = True
        while touched:
            item = Gold(
                'gold_big',
                random.randint(50, 950),
                random.randint(200, 690),
            )

            touched = False

            for i in gold_small:
                if item.touches(i):
                    touched = True
            for i in gold_small_rock:
                if item.touches(i):
                    touched = True
            for i in gold_middle:
                if item.touches(i):
                    touched = True
            for i in gold_big_rock:
                if item.touches(i):
                    touched = True
            for i in gold_large:
                if item.touches(i):
                    touched = True

        gold_large.add(item)

    # 生成钻石
    for c in range(0, random.randint(base, no_diamond)):
        touched = True
        while touched:
            item = Gold(
                'diamond',
                random.randint(50, 950),
                random.randint(200, 690),
            )

            touched = False

            for i in gold_small:
                if item.touches(i):
                    touched = True
            for i in gold_small_rock:
                if item.touches(i):
                    touched = True
            for i in gold_middle:
                if item.touches(i):
                    touched = True
            for i in gold_big_rock:
                if item.touches(i):
                    touched = True
            for i in gold_large:
                if item.touches(i):
                    touched = True
            for i in gold_diamond:
                if item.touches(i):
                    touched = True

        gold_diamond.add(item)


    # 生成随机袋子
    for c in range(0, random.randint(base, no_random)):
        touched = True
        while touched:
            item = Gold(
                'mystery_bag',
                random.randint(50, 950),
                random.randint(200, 690),
            )

            touched = False

            for i in gold_small:
                if item.touches(i):
                    touched = True
            for i in gold_small_rock:
                if item.touches(i):
                    touched = True
            for i in gold_middle:
                if item.touches(i):
                    touched = True
            for i in gold_big_rock:
                if item.touches(i):
                    touched = True
            for i in gold_large:
                if item.touches(i):
                    touched = True
            for i in gold_diamond:
                if item.touches(i):
                    touched = True
            for i in gold_random_big:
                if item.touches(i):
                    touched = True

        gold_random_big.add(item)


chainhead = Chainhead(240, 546, )

chainhead_group = pygame.sprite.Group()
chainhead_group.add(chainhead)

character= Character(455, 50, )
character_group = pygame.sprite.Group()
character_group.add(character)

# boom group
boom_group = pygame.sprite.Group()

# 开始游戏按钮
start_button_sf = pygame.Surface((170, 170))  # the size of your rect
start_button_sf.set_alpha(0)                # alpha level 透明度
# start_button_sf.fill((255,255,255))
start_button = Button(335, 200, start_button_sf)


restart_button = Button(SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2, pygame.image.load(picture_list[-1]), 2)

# print(pygame.font.get_fonts())
run = True
key_n_clicked = False

while run:

    clock.tick(FPS)

    # 背景颜色
    screen.fill('grey')

    # 场景一  开始界面
    if scene == 0:
        # screen.blit(bg, (106, 22.5))
        # 背景图片
        screen.blit(start_bg_img, (
            500 - start_bg_img.get_width() /2, # 居中
            350 - start_bg_img.get_height() /2,  # 居中
        ))
        # 提示
        draw_text(
            '按下空格键开始',
            yahei_font30,
            'red',
            350,
            500,
            # 420,
            # 450
        )
        # 轮子
        # chainhead.rect.center =  ( 240, 546 )
        chainhead.rect.center =  ( 420, 250)
        chainhead_group.update()
        chainhead_group.draw(screen)

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            scene = 2
            level_generation(level)

        if start_button.draw(screen):
            scene = 2
            level_generation(level)



    # 场景二 游戏
    if scene == 2:

        screen.blit(head_img, (0, 0, ))

        screen.blit(machine_img, (
            500 - machine_img.get_width() /2,
            37.5 - machine_img.get_width() /2 + 15,
        ))
        screen.blit(body_img, (2, 85))

        key = pygame.key.get_pressed()

        if chain_thrown_out == False:

            character.update_action(0)

            if popped_up_word_counterdown >= 16:
                if direction_left_to_right:
                    degree += 1.5
                else:
                    degree -= 1.5

            if degree <= -70:
                direction_left_to_right = True

            if degree >= 70:
                direction_left_to_right = False

            # 57.29 是一弧度
            # 半径 75
            # 计算出圆上某个点的坐标
            # pos = (
            #      500 + math.sin(degree/57.29) * 75,
            #      75 + math.cos(degree/57.29) * 75
            # )
            # 绳子的头部
            pos = (
                 500 + math.sin(math.radians(degree)) * 75,
                 75  + math.cos(math.radians(degree)) * 75
            )

            chainhead.rect.center = pos
            # 绳子
            for i in range(0, 25):
                pos = (
                     500 + math.sin(math.radians(degree)) * 2.5 * i ,
                     75  + math.cos(math.radians(degree)) * 2.5 * i ,
                )
                body_rect = pygame.Rect(pos, (5, 5))
                body_rect.center = pos

                chainbody = screen.fill('black', body_rect)

                screen.fill('black', chainbody)


        # 按下向下键时,  改变对应状态
        if (key[pygame.K_DOWN] or key[pygame.K_s]) and chain_thrown_out == False and popped_up_word_counterdown >= 16:
            chain_thrown_out = True
            chain_thrown_out_away = True
            chain_thrown_out_catchsomething = False
            chain_distance = 30

        # 按下向上按键时候,  爆破物品
        if (key[pygame.K_UP] or key[pygame.K_w]) and chain_thrown_out_catchsomething:
            chain_thrown_out_catchsomething = False
            weight_item_caught = speed + 5
            boom = Boom(chainhead.rect.centerx, chainhead.rect.centery)
            boom_group.add(boom)
            catch_gold_group.empty()

        # 绳子抛出动画
        if chain_thrown_out and chain_thrown_out_away:

            # chain_distance += speed
            chain_distance += speed - 3

            for i in range(1, chain_distance):
                pos = (
                     500 + math.sin(math.radians(degree)) * 2.5 * i ,
                     75  + math.cos(math.radians(degree)) * 2.5 * i ,
                )
                body_rect = pygame.Rect(pos, (5, 5))
                body_rect.center = pos
                chainbody = screen.fill('black', body_rect)
                screen.fill('black', chainbody)


            chainhead.rect.center = (
                500 + math.sin(math.radians(degree)) * (10 + 2.5 * chain_distance),
                70  + math.cos(math.radians(degree)) * (10 + 2.5 * chain_distance),
            )

        # 绳子回来动画
        if chain_thrown_out and chain_thrown_out_away == False:

            chain_distance -= weight_item_caught

            for i in range(1, chain_distance):
                pos = (
                     500 + math.sin(math.radians(degree)) * 2.5 *i ,
                     75  + math.cos(math.radians(degree)) * 2.5 *i ,
                )
                body_rect = pygame.Rect(pos, (5, 5))
                body_rect.center = pos
                chainbody = screen.fill('black', body_rect)
                screen.fill('black', chainbody)

            chainhead.rect.center = (
                500 + math.sin(math.radians(degree)) * (10 + 2.5 * chain_distance),
                70  + math.cos(math.radians(degree)) * (10 + 2.5 * chain_distance),
            )


        # 判断边界情况, 碰到边界后, 改变绳子来去变量
        if  chainhead.rect.centerx < 0 or chainhead.rect.centerx > 1000 or chainhead.rect.centery > 700:
            chain_thrown_out_away = False

        # 当绳子收缩到原来位置时候, 停止收缩, 继续摆动
        if chain_distance <= 29 and chain_thrown_out:
            # print('执行了')
            # 绳子抓到东西的时候, 取消抓到东西
            if chain_thrown_out_catchsomething:
                chain_thrown_out_catchsomething = False
                # 找到东西的时候 增加金钱
                if value_caught != 0:
                    popped_up_word_counterdown = 1
                money += value_caught
            chain_thrown_out = False
            weight_item_caught = speed + 5


        # print(chain_thrown_out_catchsomething, '1')

        if chain_thrown_out:
            character.update_action(1)


        popped_up_word_counterdown += 1

        # 显示游戏信息
        show_info()
        # 倒计时
        countdown()


        character_group.update()
        chainhead_group.update()

        character_group.draw(screen)
        chainhead_group.draw(screen)

        gold_middle.update()
        gold_small.update()
        gold_large.update()
        gold_diamond.update()
        gold_small_rock.update()
        gold_big_rock.update()
        gold_random_big.update()

        catch_gold_group.update()
        boom_group.update()

        gold_middle.draw(screen)
        gold_small.draw(screen)
        gold_large.draw(screen)
        gold_diamond.draw(screen)
        gold_small_rock.draw(screen)
        gold_big_rock.draw(screen)
        gold_random_big.draw(screen)

        catch_gold_group.draw(screen)
        boom_group.draw(screen)


    # 场景四 游戏失败画面
    if scene == 4:

        draw_text('GAME OVER!', yahei_font40, 'white', int(SCREEN_HEIGHT/2+48), int(SCREEN_HEIGHT/2-60))
        if restart_button.draw(screen):
            level_generation(1)
            scene = 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and not key_n_clicked:
            if event.key == pygame.K_n:
                level += 1
                if level > 12:
                    level = 0
                level_generation(level)
                key_n_clicked = True
        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_n:
                key_n_clicked = False


    pygame.display.update()


pygame.quit()


# def foo(a, b, c):
#     print('ahahah')
#     # print(type(a))
#     # print(type(b))
#     print(a)
#     print(b)

# def update(*args, **kwargs):

#     print(type(args))
#     print(type(kwargs))

#     foo(*args, **kwargs)


# update(1,2,3)
