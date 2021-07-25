import pygame
from pygame.locals import *

# 定义 fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption('Space Invanders')

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


	def draw(self):
		pass

	def update(self):

		#  移动速度
		speed = 8

		# 获取键盘按下事件
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left >0:
			self.rect.x -= speed
		if key[pygame.K_RIGHT] and self.rect.right < screen_width:
			self.rect.x += speed

		# 绘制hp
		pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom+10), self.rect.width, 15))

		if self.health_remaining > 0:
			pygame.draw.rect(
				screen, green,
				(self.rect.x, (self.rect.bottom+10),
				 int(self.rect.width*(self.health_remaining/self.health_start)),
			 15))




# 创建精灵分组
spaceship_group = pygame.sprite.Group()

# 创建玩家
spaceship = Spaceship(int(screen_width/2), screen_height - 100, 3)

spaceship_group.add(spaceship)

run = True

while run:

	clock.tick(fps)

	# 画背景
	draw_bg()

	# 事件处理
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	# 更新飞船
	spaceship.update()

	# 绘制精灵分组
	spaceship_group.draw(screen)

	pygame.display.update()

pygame.quit()
