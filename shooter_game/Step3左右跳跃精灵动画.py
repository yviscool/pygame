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

# define colours
BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():
	screen.fill(BG)
	pygame.draw.line(screen, RED, (0, 400), (SCREEN_WIDTH, 400))

class Soldier(pygame.sprite.Sprite):

	def __init__(self, char_type, x, y, scale, speed):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True
		self.char_type = char_type
		self.speed = speed
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
		animation_types = ['Idle', 'Run', 'Jump']
		for animation in animation_types:
			temp_list = []
			num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
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



player = Soldier('player', 200,  200, 3, 5)
enemy = Soldier('enemy', 400,  200, 3, 5)

run = True

while run:

	clock.tick(FPS)

	draw_bg()
	player.update_animation()
	player.draw()
	enemy.draw()

	# update player actions
	if player.alive:
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


	pygame.display.update()

pygame.quit()
