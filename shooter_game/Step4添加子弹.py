import pygame
import os

pygame.init()


clock = pygame.time.Clock()
FPS = 60



SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

# define game variables
GRAVITY =  0.75

# define player action variables
move_left = False
move_right = False
shoot = False
# load images
# bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

# define colours
BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():
	screen.fill(BG)
	pygame.draw.line(screen, RED, (0, 400), (SCREEN_WIDTH, 400))

class Soldier(pygame.sprite.Sprite):

	def __init__(self, char_type, x, y, scale, speed, ammo):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True
		self.char_type = char_type
		self.speed = speed
		self.ammo = ammo
		self.start_ammo = ammo
		self.shoot_cooldown = 0
		self.health = 100
		self.max_health = self.health
		self.direction = 1 # 1 right -1 left
		self.vel_y = 0
		self.jump = False
		self.in_air = True
		self.flip = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0 # idle 0 run 1
		self.update_time = pygame.time.get_ticks()
		# load all images for the players
		animation_types = ['Idle', 'Run', 'Jump', 'Death']
		for animation in animation_types:
			temp_list = []
			num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def move(self, move_left, move_right):

		# reset movement variables
		dx = 0
		dy = 0

		# assign movement variables if moving left or right
		if move_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1
		if move_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		# jump
		if self.jump and not self.in_air:
			self.vel_y = -11
			self.jump = False
			self.in_air = True

		# apply gravity
		self.vel_y += GRAVITY
		if self.vel_y > 10:
			self.vel_y

		dy += self.vel_y

		# check collistion with floor
		if self.rect.bottom + dy > 400:
			dy = 400 - self.rect.bottom
			self.in_air = False

		# update rectangle position
		self.rect.x += dx
		self.rect.y += dy

	def shoot(self):
		if self.shoot_cooldown == 0 and self.ammo > 0:
			self.shoot_cooldown = 20
			bullet = Bullet(self.rect.centerx+(0.6 * self.rect.size[0]*self.direction), self.rect.centery, self.direction)
			bullet_group.add(bullet)
			# reduce ammo
			self.ammo -= 1

	def update(self):

		self.update_animation()
		self.check_alive()

		# update cooldown
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1

	def check_alive(self):

		if self.health <= 0:
			self.health = 0
			self.alive = False
			self.speed = 0
			self.update_action(3)

	def update_animation(self):
		# update animation
		ANIMATION_COOLDOWN = 100
		# update image depending on current frame
		self.image = self.animation_list[self.action][self.frame_index]
		# check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.frame_index += 1
			self.update_time = pygame.time.get_ticks()
		# if the animation has run out the reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) -1
			else:
				self.frame_index = 0

	def update_action(self, new_action):
		#check if the new action is different to the previous one
		if new_action != self.action:
			self.action = new_action
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def draw(self):

		img = pygame.transform.flip(self.image, self.flip, False)
		screen.blit(img, self.rect)


class Bullet(pygame.sprite.Sprite):

	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self):
		# move speed
		self.rect.x += (self.speed * self.direction)
		# check if bullet has gone off screen
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()

		# check collision with characters
		if pygame.sprite.spritecollide(player, bullet_group, False):
			if player.alive:
				player.health -= 5
				self.kill()
		if pygame.sprite.spritecollide(enemy, bullet_group, False):
			if enemy.alive:
				enemy.health -= 25
				self.kill()
# create sprite groups
bullet_group = pygame.sprite.Group()

player = Soldier('player', 200,  200, 3, 5, 30)
enemy = Soldier('enemy', 400,  300, 3, 5, 30)

run = True

while run:

	clock.tick(FPS)

	draw_bg()
	# player.update_animation()
	player.update()
	player.draw()

	enemy.update()
	enemy.draw()

	# update and draw groups
	bullet_group.update()
	bullet_group.draw(screen)

	# update player actions
	if player.alive:
		# shoot bullets
		if shoot:
			# bullet = Bullet(player.rect.centerx+(0.6 * player.rect.size[0]*player.direction), player.rect.centery, player.direction)
			# bullet_group.add(bullet)
			player.shoot()
		if player.in_air:
			player.update_action(2) # 2: jump
		elif move_left or move_right:
			player.update_action(1) # 1: run
		else:
			player.update_action(0) # 0: idle
		player.move(move_left, move_right)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		# keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				move_left = True
			if event.key == pygame.K_d:
				move_right = True
			if event.key == pygame.K_SPACE:
				shoot = True
			if event.key == pygame.K_w and player.alive:
				player.jump = True
			if event.key == pygame.K_ESCAPE:
				run = False
		# keyboard button released
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				move_left = False
			if event.key == pygame.K_d:
				move_right = False
			if event.key == pygame.K_SPACE:
				shoot = False


	pygame.display.update()

pygame.quit()
