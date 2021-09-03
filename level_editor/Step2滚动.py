import pygame
from pygame.locals import *

pygame.init()

clock  = pygame.time.Clock()
fps = 60

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH+SIDE_MARGIN, SCREEN_HEIGHT+LOWER_MARGIN))
pygame.display.set_caption('Level Editor')


# define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS

scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

#load images
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

#define colours
GREEN = (144, 201, 12)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# create function for drawing background
def draw_bg():
	screen.fill(GREEN)
	# 这里 scroll -scroll 的原因就是不让他变成负数也就是他只能往右移动, 往左边最多只让他到 0 的位置
	width = sky_img.get_width()
	for x in range(4):
		# scroll乘于不同数是为了让他们移动有不同的层次感
		screen.blit(sky_img, ((x*width)-scroll*0.5, 0))
		screen.blit(mountain_img, ((x*width)-scroll*0.6, SCREEN_HEIGHT- mountain_img.get_height() - 300))
		screen.blit(pine1_img, ((x*width)-scroll*0.7, SCREEN_HEIGHT- pine1_img.get_height() - 150))
		screen.blit(pine2_img, ((x*width)-scroll*0.8, SCREEN_HEIGHT- pine2_img.get_height()))

# draw grid

def draw_grid():
	# 垂直
	# vertical lines
	for C in range(MAX_COLS+1):
		pygame.draw.line(screen, WHITE, (C * TILE_SIZE- scroll, 0), (C*TILE_SIZE - scroll, SCREEN_HEIGHT))

	# horizontal lines
	for C in range(ROWS+1):
		pygame.draw.line(screen, WHITE, (0, C * TILE_SIZE), ( SCREEN_HEIGHT,C*TILE_SIZE))


run = True

while run:

	clock.tick(fps)

	draw_bg()
	draw_grid()

	# scroll the map
	if scroll_left and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right:
		scroll += 5 * scroll_speed

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			run = False
		# keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1

	pygame.display.update()


pygame.quit()
