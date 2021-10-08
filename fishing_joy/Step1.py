import pygame
import random
import math
from pygame import mixer
from pygame.sprite import Sprite

mixer.init()
pygame.init()

# 首先窗口大小
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('fish')

# 设置游戏帧数
clock = pygame.time.Clock()
FPS = 60

# 播放背景音乐
pygame.mixer.music.load('audio/背景乐_02.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)


shot_fx= pygame.mixer.Sound('audio/FX_发炮_01.wav')
shot_fx.set_volume(0.5)
get_score_fx= pygame.mixer.Sound('audio/FX_获分01.wav')
get_score_fx.set_volume(0.5)

# 字体
font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 30)


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

# 背景
bg = pygame.image.load('images/bg.jpg')
# 底部栏
bar = pygame.image.load('images/bottom-bar.png').convert_alpha()
cannon_plus = pygame.image.load('images/cannon_plus.png').convert_alpha()
cannon_minus = pygame.image.load('images/cannon_minus.png').convert_alpha()





#button class
class Button():
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
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
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

# 炮台
class Cannon():

    def __init__(self):

        # self.image = pygame.image.load('images/cannon1_bck.png')
        # self.image = pygame.image.load('images/cannon1_bck.png')
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        image_height_list = [370, 380, 380, 415, 425, 450, 470]

        for i, h in enumerate(image_height_list):
            temp_list = [pygame.image.load(f'images/cannon{i+1}.png').subsurface(0, j*(h//5), 74, h//5) for j in range(0, 5)]
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.org_image = self.image.copy()
        # 中心点
        self.pos = (555, 735)
        #  旋转角度
        self.angle = 0
        self.rect = self.image.get_rect(center=self.pos)


        self.clicked = False

    def draw(self):

        screen.blit(self.image, self.rect)

    def update(self):

        self.update_animation()
        self.rotate()
        self.shot()

    # 更新动画
    def update_animation(self):

        ANIMATION_COOLDOWN = 50

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, action):

        if self.action != action:
            self.action = action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



    def rotate(self):
        # 1.通过键盘旋转角度
        # key = pygame.key.get_pressed()

        # if key[pygame.K_a]:
        #     self.angle += 1
        # if key[pygame.K_d]:
        #     self.angle -= 1

        # self.image = pygame.transform.rotate(self.org_image, self.angle)

        # self.rect = self.image.get_rect(center=self.pos)


        # 2. 通过鼠标
        # x, y = pygame.mouse.get_pos()
        # x1, y1 = self.pos
        # self.angle = math.degrees(math.atan2(-(y - y1), x - x1)) - 90
        radius, angle = (pygame.mouse.get_pos() - pygame.Vector2(self.pos)).as_polar()
        # self.angle = -angle - 90
        # print( (pygame.mouse.get_pos() - pygame.Vector2(self.pos)).as_polar())
        self.angle = angle
        # self.image = pygame.transform.rotate(self.org_image, -self.angle - 90)
        self.image = pygame.transform.rotate(self.animation_list[self.action][self.frame_index], -self.angle - 90)
        self.rect = self.image.get_rect(center=self.pos)

    def shot(self):

        mouse = pygame.mouse.get_pressed()

        if mouse[0] and not self.clicked :
            shot_fx.play()
            bullet = Bullet(self.rect.center, self.angle, self.action)
            bullet_group.add(bullet)
            self.clicked = True
            number.number -= 1

        if not mouse[0]:
            self.clicked = False

# 子弹
class Bullet(Sprite):

    def __init__(self, pos, angle, action = 0):
        Sprite.__init__(self)

        # self.image = pygame.image.load('images/bullet1.png')
        self.animation_list = []
        self.action = action
        self.update_time = pygame.time.get_ticks()
        for i in range(1, 8):
            img = pygame.image.load(f'images/bullet{i}.png')
            self.animation_list.append(img)

        self.image = self.animation_list[self.action]
        # self.org_image = self.image.copy()
        self.angle = angle

        self.image = pygame.transform.rotate(self.image, -self.angle-90)
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0]+3, pos[1])

        self.speed = 10

        radians = math.radians(-self.angle)

        self.dx = math.cos(radians) * self.speed
        self.dy = -(math.sin(radians) * self.speed)

    def update(self):

        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.right < 0 or self.rect.left > 1024 or self.rect.bottom < 0:
            self.kill()
# 鱼类
class Fish(Sprite):

    def __init__(self):
        Sprite.__init__(self)

        self.speed = 2
        self.animation_list = []
        self.frame_index = 0
        # 分数奖励
        self.reward = 15
        self.direction = random.choice([1, -1]) # 1 右边 -1 左边
        self.action = 0  # 0 alive , 1 death
        self.flip = False if self.direction == 1 else True # 是否左右反转
        self.update_time = pygame.time.get_ticks()
        self.alive = True

        sheet  = pygame.image.load('images/fish1.png')

        width = sheet.get_width() / 1
        height = sheet.get_height() / 8

        # 加载alive动画
        temp_list  = []
        for row in range(4):
            clip = pygame.Rect(
                0,
                row * height,
                width,
                height
            )
            frame = sheet.subsurface(clip)
            temp_list.append(frame)

        self.animation_list.append(temp_list)

        # 加载死亡动画
        temp_list = []
        for row in range(4, 8):
            clip = pygame.Rect(
                0,
                row * height,
                width,
                height
            )
            frame = sheet.subsurface(clip)
            temp_list.append(frame)

        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.center = (
            0 if self.direction == 1 else 1024,
            random.randint(10, 700)
        )


    def update(self):

        # 向右
        if self.direction == 1:
            self.rect.x += self.speed
        # 向左
        else:
            self.rect.x -= self.speed

        # pygame.sprite.groupcollide(bullet_group, fish_group, True, True)
        if self.alive:
            if pygame.sprite.spritecollide(self, bullet_group, True):
                # 死亡
                self.update_action(1)
                # 移动速度变成 0
                self.speed = 0
                self.alive = False
                # 捕鱼网
                net = Net(self.rect)
                net_group.add(net)
                # 金币奖励文本
                cointext = Cointext(self.rect.topleft, 5)
                cointext_group.add(cointext)
                for count, i in enumerate(list(map(int, str(self.reward)))):
                    c = Cointext((self.rect.x+(count+1)*36, self.rect.y), 1, i)
                    cointext_group.add(c)
                # 金币收集效果
                coin = Coin(self.rect.topleft)
                coin_group.add(coin)
                get_score_fx.play()

        # 更新鱼动画
        self.update_animation()

        # 鱼越界
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

    def update_animation(self):

        ANIMATION_COOLDOWN = 100

        self.image = self.animation_list[self.action][self.frame_index]

        self.image= pygame.transform.flip(self.image, self.flip, False)

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            # 死鱼
            if self.action == 1:
                # 死亡后, 移除
                self.frame_index = len(self.animation_list[self.action]) -1
                self.kill()
            else:
                self.frame_index = 0

    def update_action(self, action):

        if self.action != action:
            self.action = action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


# 网
class Net(pygame.sprite.Sprite):

    def __init__(self, rect):

        Sprite.__init__(self)

        self.image = pygame.image.load('images/web1.png')
        self.rect = rect
        self.counter = 0
        self.update_time = pygame.time.get_ticks()



    def update(self):



        self.image = pygame.transform.smoothscale(self.image, (
            self.image.get_width()  + 5,
            self.image.get_height() + 5,
        ))


        if pygame.time.get_ticks() - self.update_time > 300:
            self.kill()


# 金币奖励
class Cointext(Sprite):
    def __init__(self, rect, reward=5, index=10):
        Sprite.__init__(self)
        self.images = [pygame.image.load('images/coinText.png').subsurface(i*36, 0, 36, 49) for i in range(0, 11)]
        self.rect = rect
        # self.reward = reward
        self.counter = 0
        self.image = self.images[index]

    # def draw(self):

    #     for count, i in enumerate(self.change()):
            # screen.blit(self.images[i], (self.rect[0]+count*36, self.rect[1]))

    # def change(self):
    #     l = list(map(int, str(self.reward)))
    #     ##每个数字前插入X
    #     l.insert(0,10)
    #     return l

    def update(self):

        self.counter += 1

        if self.counter > 50:
            self.kill()

# 金币收集效果
class Coin(Sprite):
    def __init__(self, target_center):
        Sprite.__init__(self)
        self.images = [pygame.image.load('images/coinAni1.png').subsurface(0, i*60, 60, 60) for i in range(0, 10)]
        self.index = 0
        self.image = self.images[self.index]
        self.update_time = pygame.time.get_ticks()

        self.coin_end_pos = (200, 724)

        radius, angle = (self.coin_end_pos - pygame.Vector2(target_center)).as_polar()

        self.angle = angle
        self.rect = self.image.get_rect()
        self.rect.center = target_center

        self.speed = 5

        radians = math.radians(self.angle)

        self.dx = math.cos(radians) * self.speed
        self.dy = (math.sin(radians) * self.speed)

        # print(self.angle, self.dx, self.dy)

    def update(self):

        self.update_animation()

        self.rect.x += self.dx
        self.rect.y += self.dy

        # if self.rect.collidepoint(self.coin_end_pos):
        if self.rect.bottom > 700:
            self.kill()

    def update_animation(self):

        ANIMATION_COOLDOWN = 30

        self.image = self.images[self.index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.index += 1
            self.update_time = pygame.time.get_ticks()

        if self.index >= len(self.images) -1:
            self.index = 0


# 分数栏
class Number():

    def __init__(self):

        # 因为数字是 9 8 7 6 5 4 3 2 1 0
        # 但是访问对应数字的索引是 0 1 2 3 4 5 6 7 8 9
        # 一种方法是对 9-0 进行反转, 这样就能匹配,
        # 第二种就是对索引进行反转 使用 abs(i-9) 即可
        self.animation_list = [pygame.image.load('images/number_black.png').subsurface(0, i*24, 20, 24) for i in range(0, 10)]
        self.animation_list.reverse()
        self.frame_index = 0
        self.image = self.animation_list[self.frame_index]
        self.number = 709394

    def draw(self):

        count = 0
        for i in self.change(self.number):
            screen.blit(self.animation_list[i], (150+23*count, 740))
            count += 1

    def change(self, number):

        l = list(map(int, str(number)))

        # 如果不足六位, 在头部插入
        if len(l) < 6:
            for i in range(0, 6-len(l)):
                l.insert(0, 0)

        # result = []
        # for n in l:
        #     result.append(abs(n-9))

        # print(result)
        # return result
        return l




cannon = Cannon()
number = Number()

bullet_group = pygame.sprite.Group()
fish_group = pygame.sprite.Group()
net_group = pygame.sprite.Group()
cointext_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()


cannon_plus_btn = Button(590, 730, cannon_plus)
cannon_minus_btn = Button(480, 730, cannon_minus)

run = True

# for i in range(50):
#     fish = Fish()
#     fish_group.add(
#         fish
#     )

# 随机定时产生鱼, 即设置一个事件定时器
PRODUCT_FISH_EVENT = pygame.USEREVENT + 1

# 每隔 1 秒,  PRODUCT_FISH_EVENT 出现在队列里面
pygame.time.set_timer(PRODUCT_FISH_EVENT, 1000)

# coin = Cointext(pygame.Rect(200,200, 30, 30), 5)

# coin = Coin((300, 300))
# coin_group.add(coin)


while run:

    clock.tick(FPS)

    # 背景颜色
    screen.blit(bg, (0, 0))
    # 绘制状态栏
    screen.blit(bar, (
            (SCREEN_WIDTH - bar.get_width()) // 2,
            SCREEN_HEIGHT - bar.get_height(),
        )
    )

    number.draw()

    if cannon_plus_btn.draw():
        # if cannon.action>=6:
        #     cannon.update_action(6)
        # else:
        #     cannon.update_action(cannon.action+1)
        cannon.update_action(
            6 if cannon.action >= 6  else cannon.action +1
        )
    if cannon_minus_btn.draw():
        # if cannon <= 0:
        #     cannon.update_action(0)
        # else:
        #     cannon.update_action(cannon.action-1)
        cannon.update_action(
            0 if cannon.action <= 0 else cannon.action - 1
        )


    bullet_group.update()
    fish_group.update()
    net_group.update()
    cointext_group.update()
    coin_group.update()

    bullet_group.draw(screen)
    fish_group.draw(screen)
    net_group.draw(screen)
    cointext_group.draw(screen)
    coin_group.draw(screen)

    cannon.update()
    cannon.draw()


    # pygame.sprite.groupcollide(bullet_group, fish_group, True, True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == PRODUCT_FISH_EVENT:
            fish = Fish()
            fish_group.add(
                fish
            )
    pygame.display.update()


pygame.quit()

