import pygame
import math
import random
import os
from enemy import Enemy
import button

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Castle Defender')

clock = pygame.time.Clock()
FPS = 60


# define game variables
high_score = 0
level = 1
level_difficulty = 0
target_difficulty = 1000
DIFFICULTY_MULTIPLIER = 1.1
game_over = False
next_level = False
# MAX_ENEMIES = 10
ENEMY_TIMER = 1000
last_enemy = pygame.time.get_ticks()
enemy_alive = 0
TOWER_COST = 5000
tower_position = [
	[SCREEN_WIDTH - 250, SCREEN_HEIGHT - 200],
	[SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150],
	[SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150],
	[SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150],
]
max_towers = 4


# load high score
if os.path.exists('score.txt'):
	with open('score.txt', 'r') as file:
		high_score = int(file.read())

# define colours
WHITE = (255, 255, 255)
GREY = (100, 100, 100)


# define font
font = pygame.font.SysFont('Futura', 30)
font_60 = pygame.font.SysFont('Futura', 60)

# load images
bg = pygame.image.load('img/bg.png').convert_alpha()
# cestle
castle_img_100 = pygame.image.load('img/castle/castle_100.png').convert_alpha()
castle_img_50 = pygame.image.load('img/castle/castle_50.png').convert_alpha()
castle_img_25 = pygame.image.load('img/castle/castle_25.png').convert_alpha()

#tower

tower_img_100 = pygame.image.load('img/tower/tower_100.png').convert_alpha()
tower_img_50 = pygame.image.load('img/tower/tower_50.png').convert_alpha()
tower_img_25 = pygame.image.load('img/tower/tower_25.png').convert_alpha()

# bullet_image
bullet_img = pygame.image.load('img/bullet.png')
bullet1_img = pygame.image.load('img/bullet1.png')
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w*0.075), int(b_h*0.075)))

# load enemies
enemy_animations = []
enemy_types = [ 'knight', 'goblin', 'purple_goblin', 'red_goblin']
enemy_health = [ 75, 100, 125, 150 ]

animation_types = [ 'walk', 'attack', 'death']

for enemy in enemy_types:
	# load animation
	animation_list = []
	for animation in animation_types:
		# reset temporary list of images
		temp_list = []
		num_of_frames = 20
		for i in range(num_of_frames):
			img = pygame.image.load(f'img/enemies/{enemy}/{animation}/{i}.png').convert_alpha()
			e_w = img.get_width()
			e_h = img.get_height()
			img = pygame.transform.scale(img, (int(e_w*0.2), int(e_h*0.2)))
			temp_list.append(img)
		animation_list.append(temp_list)
	enemy_animations.append(animation_list)

# button images
repair_img = pygame.image.load('img/repair.png').convert_alpha()
armour_img = pygame.image.load('img/armour.png').convert_alpha()


# castel class
class Castle():

	def __init__(self, image100, image50, image25, x, y, scale):
		self.health = 1000
		self.max_health = self.health
		self.fired = False
		self.money = 50000
		self.score = 0

		width = image100.get_width()
		height = image100.get_height()

		self.image100 = pygame.transform.scale(image100, (int(width*scale), int(height * scale)))
		self.image50 = pygame.transform.scale(image50, (int(width*scale), int(height * scale)))
		self.image25 = pygame.transform.scale(image25, (int(width*scale), int(height * scale)))
		self.rect = self.image100.get_rect()
		# self.rect.x = x
		# self.rect.y = y
		self.rect.topleft = (x, y)

	def shoot(self):
		pos = pygame.mouse.get_pos()
		x_dist = pos[0] - self.rect.midleft[0]
		y_dist = -(pos[1] - self.rect.midleft[1])
		self.angle = math.degrees(math.atan2(y_dist, x_dist))
		# get mouseclick
		# if pygame.mouse.get_pressed()[0] and self.fired == False:
		if pygame.mouse.get_pressed()[0] and self.fired == False and pos[1] > 70:
			self.fired = True
			bullet = Bullet(bullet1_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
			bullet_group.add(bullet)
		# reset mouseclick
		if pygame.mouse.get_pressed()[0] == False:
			self.fired = False

		# pygame.draw.line(screen, WHITE, (self.rect.midleft[0], self.rect.midleft[1]), (pos))

	def draw(self):
		# check which image to use based on health
		if self.health <= 250:
			self.image = self.image25
		elif self.health <= 500:
			self.image = self.image50
		else:
			self.image = self.image100

		screen.blit(self.image, self.rect)

	def repair(self):

		if self.money >= 1000 and self.health < self.max_health:
			self.health += 500
			self.money -= 500
			if self.health > self.max_health:
				self.health = self.max_health


	# 升级最大生命值
	def armour(self):

		if self.money >= 500:
			self.max_health += 250
			self.money -= 500

# function for ouputing text onto the screen

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# function for displaying status

def show_info():
	draw_text('Money: ' + str(castle.money), font, GREY, 10, 10)
	draw_text('Score: ' + str(castle.score), font, GREY, 180, 10)
	draw_text('Hight Score: ' + str(high_score), font, GREY, 180, 30)
	draw_text('Level: ' + str(level), font, GREY, SCREEN_WIDTH//2, 10)
	draw_text('Health: ' + str(castle.health) + ' / ' + str(castle.max_health), font, GREY, SCREEN_WIDTH-230, SCREEN_HEIGHT - 50)
	draw_text('1000', font, GREY, SCREEN_WIDTH - 200, 70)
	draw_text('500', font, GREY, SCREEN_WIDTH - 70, 70)
	draw_text('5000', font, GREY, SCREEN_WIDTH - 130, 70)


# tower class

class Tower(pygame.sprite.Sprite):

	def __init__(self, image100, image50, image25, x, y, scale):
		pygame.sprite.Sprite.__init__(self)

		self.got_target = False
		self.angle = 0
		self.last_shot = pygame.time.get_ticks()
		self.shoot_cooldown = 1000

		width = image100.get_width()
		height = image100.get_height()

		self.image100 = pygame.transform.scale(image100, (int(width*scale), int(height * scale)))
		self.image50 = pygame.transform.scale(image50, (int(width*scale), int(height * scale)))
		self.image25 = pygame.transform.scale(image25, (int(width*scale), int(height * scale)))
		self.image = self.image100
		self.rect = self.image100.get_rect()
		self.rect.topleft = (x, y)

	# def draw(self):
	# 	screen.blit(screen, self.rect)

	def update(self, enemy_group):

		self.got_target = False

		# 找到前排第一个敌人
		for e in enemy_group:
			if e.alive:
				target_x, target_y = e.rect.midbottom
				self.got_target = True
				break

		if self.got_target:
			# pygame.draw.line(screen, WHITE, (self.rect.midleft[0], self.rect.midleft[1]), (target_x, target_y))
			pos = pygame.mouse.get_pos()
			x_dist = target_x - self.rect.midleft[0]
			y_dist = -(target_y - self.rect.midleft[1])
			self.angle = math.degrees(math.atan2(y_dist, x_dist))
			if abs(self.rect.x - target_x) < 500:
				if pygame.time.get_ticks() - self.last_shot > self.shoot_cooldown:
					bullet = Bullet(bullet1_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
					bullet_group.add(bullet)
					self.last_shot = pygame.time.get_ticks()

		if castle.health <= 250:
			self.image = self.image25
		elif castle.health <= 500:
			self.image = self.image50
		else:
			self.image = self.image100

# bullet class
class Bullet(pygame.sprite.Sprite):

	def __init__(self, image, x, y, angle):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		#
		self.angle = math.radians(angle) # convert input angle into radians
		self.speed = 10
		# calculate the horizontal and vertical speeds based on the angle

		self.dx = math.cos(self.angle) * self.speed
		self.dy = -(math.sin(self.angle) * self.speed)

		self.image =pygame.transform.rotate(image, angle - 90)

	def update(self):

		# check if bullet has gone off the screen
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH \
			or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
			self.kill()

		# move bullet
		self.rect.x += self.dx
		self.rect.y += self.dy


class Crosshair():

	def __init__(self, scale):
		image = pygame.image.load('img/crosshair.png').convert_alpha()
		width = image.get_width()
		height = image.get_height()

		self.image = pygame.transform.scale(image, (int(width*scale), int(height* scale)))
		self.rect = self.image.get_rect()

		# hide mouse
		pygame.mouse.set_visible(False)

	def draw(self):
		mx, my = pygame.mouse.get_pos()
		self.rect.center = (mx, my)
		screen.blit(self.image, self.rect)


# create castle
castle = Castle(castle_img_100, castle_img_50, castle_img_25, SCREEN_WIDTH-250,SCREEN_HEIGHT-300, 0.2)
# create crosshair
crosshair = Crosshair(0.025)
# create groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tower_group = pygame.sprite.Group()

# create button
repair_button = button.Button(SCREEN_WIDTH - 200, 10, repair_img, 0.5)
armour_button = button.Button(SCREEN_WIDTH - 75, 10, armour_img, 1.5)
tower_button = button.Button(SCREEN_WIDTH - 120, 10, tower_img_100, 0.1)

# create enemies
# enemy_1 = Enemy(enemy_health[0], enemy_animations[0], 400, SCREEN_HEIGHT - 100, 5)
# enemy_group.add(enemy_1)

# temporary tower

# tower = Tower(
# 	tower_img_100,
# 	tower_img_50,
# 	tower_img_25,
# 	# SCREEN_WIDTH-250,
# 	# SCREEN_HEIGHT - 300,
# 	tower_position[0][0],
# 	tower_position[0][1],
# 	0.2
# )

# tower_group.add(tower)

run = True
while run:

	clock.tick(FPS)

	if game_over == False:

		screen.blit(bg, (0, 0))

		# draw castle
		castle.draw()
		castle.shoot()

		# draw tower
		tower_group.draw(screen)
		tower_group.update(enemy_group)

		# draw crosshair
		crosshair.draw()

		# draw bullets
		bullet_group.update()
		bullet_group.draw(screen)

		enemy_group.update(screen, castle, bullet_group)
		# bullet_group.draw(screen)

		# show details
		show_info()

		# draw button
		if repair_button.draw(screen):
			castle.repair()
		if armour_button.draw(screen):
			castle.armour()
		if tower_button.draw(screen):
			if castle.money >= TOWER_COST and len(tower_group) < max_towers:
				tower = Tower(
					tower_img_100,
					tower_img_50,
					tower_img_25,
					tower_position[len(tower_group)][0],
					tower_position[len(tower_group)][1],
					0.2
				)
				tower_group.add(tower)
				# subtract money
				castle.money -= TOWER_COST


		# create enemies
		# check if max number of enemies has been reached

		# if len(enemy_group) < MAX_ENEMIES:
		if level_difficulty < target_difficulty:

			if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:
				e = random.randint(0, len(enemy_types) - 1)
				enemy = Enemy(enemy_health[e], enemy_animations[e], -100, SCREEN_HEIGHT - 100, 1)
				enemy_group.add(enemy)
				# reset enemy timer
				last_enemy = pygame.time.get_ticks()
				# incrase level difficulty
				level_difficulty += enemy_health[e]


		# check if all the enemies have been spawned
		if level_difficulty >= target_difficulty:
			# check how many are still alive
			enemies_alive = 0
			for e in enemy_group:
				if e.alive:
					enemies_alive += 1
			# if there are noone alive the level is completde
			if  enemies_alive == 0 and not next_level:
				next_level = True
				level_reset_time = pygame.time.get_ticks()

		# move onto the next level
		if next_level:
			draw_text('LEVEL COMPLETE!', font_60, WHITE, 200, 300)
			# update high score
			if castle.score > high_score :
				high_score = castle.score
				with open('score.txt', 'w') as file:
					file.write(str(high_score))
			if pygame.time.get_ticks() - level_reset_time > 1500:
				next_level = False
				level += 1
				last_enemy = pygame.time.get_ticks()
				target_difficulty *= DIFFICULTY_MULTIPLIER
				level_difficulty = 0
				enemy_group.empty()

		# check game over
		if castle.health <= 0:
			game_over = True
	else:
		draw_text('GAME OVER!', font, GREY, 300, 300)
		draw_text('PRESS "A" TO PLAY AGAIN ', font, GREY, 250, 360)
		pygame.mouse.set_visible(True)
		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			game_over = False
			enemy_group.empty()
			tower_group.empty()
			castle.score = 0
			castle.health = 1000
			castle.max_health = castle.health
			castle.money = 0
			level = 1
			target_difficulty = 1000
			level_difficulty =0
			last_enemy = pygame.time.get_ticks()
			pygame.mouse.set_visible(False)



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()


pygame.quit()
