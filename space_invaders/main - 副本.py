import pygame
import random
from pygame.locals import *

clock = pygame.time.Clock()

fps  = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))

run = True

red = (255, 0, 0)
green = (0, 255, 0)
rows = 5
cols = 5
aliens_bullet_cooldown = 1000
last_alien_shot = pygame.time.get_ticks()

bg = pygame.image.load('img/bg.png')

pygame.display.set_caption('Space Invanders')

def draw_bg():
	screen.blit(bg, (0,0))

class SpaceShip(pygame.sprite.Sprite):

	def __init__(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/spaceship.png')
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.health_start = health
		self.health_remaining = health
		self.last_shot = pygame.time.get_ticks()

	def update(self):

		speed = 5

		cooldown = 500 # 毫秒

		key = pygame.key.get_pressed()

		time_now = pygame.time.get_ticks()


		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x  -= speed
		if key[pygame.K_RIGHT] and self.rect.right < screen_width:
			self.rect.x  += speed
		if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
			bullet = Bullets(int(self.rect.left+self.rect.width/2), int(self.rect.y+10))
			bullets_group.add(bullet)
			self.last_shot = time_now

		pygame.draw.rect(screen, red, (self.rect.x, self.rect.bottom+10, self.rect.width, 15))

		if self.health_remaining > 0:
			pygame.draw.rect(screen, green, (self.rect.x, self.rect.bottom+10, int(self.rect.width*(self .health_remaining/self.health_start)), 15))

class Bullets(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/bullet.png')
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

	def update(self):
		speed = 5
		self.rect.y -= speed
		if self.rect.y < 0:
			self.kill()

class Aliens(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/alien'+str(random.randint(1,5))+'.png')
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.move_direction = 1
		self.move_counter = 0

	def update(self):

		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 75:
			self.move_direction *=  -1
			self.move_counter *= self.move_direction

class Aliens_Bullets(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/alien_bullet.png')
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

	def update(self):
		speed = 3
		self.rect.y += speed
		if self.rect.y > screen_height:
			self.kill()

spaceship_group = pygame.sprite.Group()
spaceship =  SpaceShip(int(screen_width/2), int(screen_height/2 + 200), 3)

spaceship_group.add(spaceship)
bullets_group = pygame.sprite.Group()
aliens_group = pygame.sprite.Group()
aliens_bullets_group = pygame.sprite.Group()

def create_aliens():
	for y in range(rows):
		for x in range(cols):
			alien = Aliens(100+x*100, y*70+100)
			aliens_group.add(alien)


create_aliens()

# print(len(aliens_group.sprites()))

while run:

	clock.tick(fps)

	draw_bg()

	time_now = pygame.time.get_ticks()

	if time_now -  last_alien_shot > 1000 and len(aliens_group) > 0:
		alien = random.choice(aliens_group.sprites())
		aliens_bullet = Aliens_Bullets(alien.rect.centerx, alien.rect.bottom)
		aliens_bullets_group.add(aliens_bullet)
		last_alien_shot = time_now


	spaceship_group.update()
	bullets_group.update()
	aliens_group.update()
	aliens_bullets_group.update()

	spaceship_group.draw(screen)
	bullets_group.draw(screen)
	aliens_group.draw(screen)
	aliens_bullets_group.draw(screen)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()


pygame.quit()
