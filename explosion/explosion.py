import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Explosion Demo')

#define colours
bg = (50, 50, 50)

def draw_bg():
	screen.fill(bg)

# 创建爆炸类
class Explosion(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"img/exp{num}.png")
			# 缩放
			img = pygame.transform.scale(img, (100, 100))
			self.images.append(img)

		self.index = 0
		self.image = self.images[self.index]
		# pygame 将会从图像创造一个矩形
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):

		# 控制动画速度
		explosion_speed = 4

		self.counter += 1

		# 播放下一个爆炸动画
		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			# print(self.counter, self.index, self.image)
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()


explosion_group  = pygame.sprite.Group()


run = True
while run:

	clock.tick(fps)

	#draw background
	draw_bg()

	explosion_group.draw(screen)
	explosion_group.update()


	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			# x, y = pos
			e = Explosion(*pos)
			explosion_group.add(e)


	pygame.display.update()

pygame.quit()	
