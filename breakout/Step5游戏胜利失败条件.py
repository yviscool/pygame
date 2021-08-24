import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

font = pygame.font.SysFont('Constantlia',30)

bg = (234, 218, 184)
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)

paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)

text_col = (78, 81, 139)


cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0


# function for outputing text onto the screen

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


class Wall():

	def __init__(self):
		self.width = screen_width // cols
		self.height = 50
		self.create_wall()

	def create_wall(self):
		self.blocks = []
		block_individual = []
		for row in range(rows):
			block_row = []
			for col in range(cols):
				block_x = col * self.width
				block_y = row * self.height
				rect = pygame.Rect(block_x, block_y,self.width, self.height)
				if row < 2:
					strength = 3
				elif row < 4:
					strength = 2
				elif row < 6:
					strength = 1
				block_individual = [rect, strength]
				block_row.append(block_individual)

			self.blocks.append(block_row)

	def draw(self):

		for row in self.blocks:
			for block in row:
				if block[1] == 3:
					block_col = block_blue
				elif block[1] == 2:
					block_col = block_green
				elif block[1] == 1:
					block_col = block_red
				pygame.draw.rect(screen, block_col, block[0])
				# 使用背景颜色填充 边框为5 的矩形
				pygame.draw.rect(screen, bg, (block[0]), 5)


class Paddle():

	def __init__(self):
		# self.width = int(screen_width/cols)
		# self.height = 20
		# self.x = int((screen_width/2)-(self.width/2))
		# self.y = screen_height - (self.height*2)
		# self.speed = 10
		# self.rect = Rect(self.x, self.y, self.width, self.height)
		# self.direction = 0
		self.reset()

	def move(self):

		self.direction = 0

		key = pygame.key.get_pressed()

		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= self.speed
			self.direction = -1
		if key[pygame.K_RIGHT] and self.rect.right < screen_width:
			self.rect.x += self.speed
			self.direction = 1

	def draw(self):

		pygame.draw.rect(screen, paddle_col, self.rect)
		pygame.draw.rect(screen, paddle_outline, self.rect, 3)

	def reset(self):
		self.width = int(screen_width/cols)
		self.height = 20
		self.x = int((screen_width/2)-(self.width/2))
		self.y = screen_height - (self.height*2)
		self.speed = 10
		self.rect = Rect(self.x, self.y, self.width, self.height)
		self.direction = 0

class Ball():

	def __init__(self, x, y):
		# self.rad = 10
		# self.x = x - self.rad
		# self.y = y
		# self.rect = Rect(self.x, self.y, self.rad*2, self.rad*2)
		# self.speed_x = 4
		# self.speed_y = -4
		# self.speed_max = 5
		# self.game_over = 0
		self.reset(x, y)

	def move(self):
		# collision threshold
		collision_thresh = 5
		# start off with the assumption that the wall has ben destoryed completely
		wall_destoryed = 1
		row_count = 0
		for row in wall.blocks:
			item_count = 0
			for item in row:
				if self.rect.colliderect(item[0]):
					# check if collision was from above
					if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
						self.speed_y *= -1
					# check if collision was from below
					if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
						self.speed_y *= -1
					# check if collision was from left
					if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
						self.speed_x *= -1
					# check if collision was from right
					if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
						self.speed_x *= -1
					if wall.blocks[row_count][item_count][1] > 1:
						wall.blocks[row_count][item_count][1] -= 1
					else:
						wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

				#check if block still exists, in whcih case the wall is not destroyed
				if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
					wall_destoryed = 0

				item_count += 1
			row_count += 1

		# after iterating throught all blocks
		if wall_destoryed == 1:
			self.game_over = 1


		# check for collision with balls
		if self.rect.left < 0 or self.rect.right > screen_width:
			self.speed_x *= -1
		# check for collision with top and bottom of the screen
		if self.rect.top < 0:
			self.speed_y *= -1
		if self.rect.bottom > screen_width:
			self.game_over = -1

		# look for collission with paddle
		if self.rect.colliderect(paddle):
			# check if collding from the top
			if abs(self.rect.bottom - paddle.rect.top) < collision_thresh and self.speed_y > 0:
				self.speed_y *= -1
				self.speed_x += paddle.direction
				if self.speed_x > self.speed_max:
					self.speed_x = self.speed_max
				elif self.speed_x < 0 and self.speed_x < -self.speed_max:
					self.speed_x = -self.speed_max
			else:
				self.speed_x *= -1

		self.rect.x += self.speed_x
		self.rect.y += self.speed_y

		return self.game_over

	def draw(self):

		pygame.draw.circle(screen, paddle_col, (self.rect.x+self.rad, self.rect.y+self.rad), self.rad)
		pygame.draw.circle(screen, paddle_outline, (self.rect.x+self.rad, self.rect.y+self.rad), 3)

	def reset(self, x, y):
		self.rad = 10
		self.x = x - self.rad
		self.y = y
		self.rect = Rect(self.x, self.y, self.rad*2, self.rad*2)
		self.speed_x = 4
		self.speed_y = -4
		self.speed_max = 5
		self.game_over = 0



run = True

wall = Wall()
paddle = Paddle()
ball = Ball(paddle.x + paddle.width//2, paddle.y - paddle.height)

while run:

	clock.tick(fps)
	screen.fill(bg)

	wall.draw()
	paddle.draw()
	ball.draw()

	if live_ball:
		paddle.move()
		game_over = ball.move()
		print(game_over)
		if game_over != 0:
			live_ball = False

	if not live_ball:
		if game_over == 0:
			draw_text('CLICK ANYWHERE TO START,', font, text_col, 150, screen_height//2+100)
		elif game_over == 1:
			draw_text('YOU WIN,', font, text_col, 150, screen_height//2+50)
			draw_text('CLICK ANYWHERE TO START,', font, text_col, 150, screen_height//2+100)
		else:
			draw_text('YOU LOSE!,', font, text_col, 240, screen_height//2+50)
			draw_text('CLICK ANYWHERE TO START,', font, text_col, 150, screen_height//2+100)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
			live_ball = True
			ball.reset(paddle.x + paddle.width//2, paddle.y - paddle.height)
			paddle.reset()
			wall.create_wall()

	pygame.display.update()

pygame.quit()
