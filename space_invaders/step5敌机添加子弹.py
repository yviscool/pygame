import pygame
from pygame.locals import *
import random

# 定义 fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption('Space Invanders')

# 定义游戏变量
rows = 5
cols = 5
alien_cooldown = 1000
last_alien_shot = pygame.time.get_ticks()

# 定义颜色
red = (255, 0, 0)
green = (0, 255, 0)

bg = pygame.image.load('img/bg.png')

def draw_bg():
	screen.blit(bg, (0,0))

# 创建飞船类
class Spaceship(pygame.sprite.Sprite):
	def __init__(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/spaceship.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.health_start = health
		self.health_remaining =  health
		self.last_shot = pygame.time.get_ticks()

	def update(self):

		#  移动速度
		speed = 8

		# 冷却时间
		cooldown = 500 # 毫秒

		# 获取键盘按下事件
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left >0:
			self.rect.x -= speed
		if key[pygame.K_RIGHT] and self.rect.right < screen_width:
			self.rect.x += speed
		# 记录时间
		time_now = pygame.time.get_ticks()
		# 射击
		if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
			bullet = Bullets(self.rect.centerx, self.rect.top)
			bullet_group.add(bullet)
			self.last_shot = time_now

		# 绘制hp
		pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom+10), self.rect.width, 15))

		if self.health_remaining > 0:
			pygame.draw.rect(
				screen, green,
				(self.rect.x, (self.rect.bottom+10),
				 int(self.rect.width*(self.health_remaining/self.health_start)),
			 15))

# 创建子弹类
class Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/bullet.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):

		self.rect.y -= 5

		if self.rect.bottom<0:
			self.kill()



# 创建敌机
class Aliens(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/alien'+str(random.randint(1,5))+'.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.move_counter = 0
		self.move_direction = 1

	def update(self):

		self.rect.x +=  self.move_direction
		self.move_counter += 1

		if abs(self.move_counter) > 75:
			self.move_direction *= -1
			self.move_counter *= self.move_direction

# 创建敌机子弹类
class Alien_Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/alien_bullet.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):

		self.rect.y += 2

		if self.rect.top > screen_height:
			self.kill()


# 创建精灵分组
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()

def create_aliens():
	# 生成敌机
	for row in range(rows):
		for item in range(cols):
			alien = Aliens(100+item*100, row*70+100)
			alien_group.add(alien)

create_aliens()

# 创建玩家
spaceship = Spaceship(int(screen_width/2), screen_height - 100, 3)

spaceship_group.add(spaceship)

run = True

while run:

	clock.tick(fps)

	# 画背景
	draw_bg()

	# 创建一个敌机子弹
	time_now  = pygame.time.get_ticks()

	if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
		attacking_alien = random.choice(alien_group.sprites())
		alien_bullt = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
		alien_bullet_group.add(alien_bullt)
		last_alien_shot = time_now


	# 事件处理
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	# 更新飞船
	spaceship.update()

	# 更新子弹
	bullet_group.update()

	#更新敌机
	alien_group.update()

	# 更新敌机子弹
	alien_bullet_group.update()

	# 绘制精灵分组
	spaceship_group.draw(screen)
	bullet_group.draw(screen)
	alien_group.draw(screen)
	alien_bullet_group.draw(screen)

	pygame.display.update()

pygame.quit()
