import pygame

pygame.init()


clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

# define player action variables
move_left = False
move_right = False

# define colours
BG = (144, 201, 120)

def draw_bg():
	screen.fill(BG)

class Soldier(pygame.sprite.Sprite):

	def __init__(self, char_type, x, y, scale, speed):
		pygame.sprite.Sprite.__init__(self)
		self.char_type = char_type
		self.speed = speed
		self.direction = 1 # 1 right -1 left
		self.flip = False
		img = pygame.image.load(f'img/{self.char_type}/Idle/0.png')
		self.image = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
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

		# update rectangle position
		self.rect.x += dx
		self.rect.y += dy

	def draw(self):

		img = pygame.transform.flip(self.image, self.flip, False)
		screen.blit(img, self.rect)



player = Soldier('player', 200,  200, 3, 5)
enemy = Soldier('enemy', 400,  200, 3, 5)

run = True

while run:

	clock.tick(FPS)

	draw_bg()

	player.draw()
	enemy.draw()
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
