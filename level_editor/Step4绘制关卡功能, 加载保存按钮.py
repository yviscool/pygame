import pygame
import button
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
TILE_TYPES = 21
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

#load images
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

# store tiles in a list
img_list = []

for x in range(TILE_TYPES):
	img = pygame.image.load(f'img//tile/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img =  pygame.image.load('img/load_btn.png').convert_alpha()

#define colours
GREEN = (144, 201, 12)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# define font
font = pygame.font.SysFont('Futura', 30)

# create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)

# create ground
for tile in range(0, MAX_COLS):
	world_data[ROWS-1][tile] = 0

# funciton for ouputing text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# funciton for drawing the world tiles
def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				# screen.blit(img_list[0], (x*TILE_SIZE-scroll, y * TILE_SIZE))
				screen.blit(img_list[tile], (x*TILE_SIZE-scroll, y * TILE_SIZE))

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


# create buttons
save_button = button.Button(SCREEN_WIDTH//2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH//2+200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
# make a button list
button_list = []
button_col = 0
button_row = 0

for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (75*button_col) + 50, 75 * button_row+50, img_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0




run = True

while run:

	clock.tick(fps)

	draw_bg()
	draw_grid()
	draw_world()

	# save and load data
	save_button.draw(screen)
	load_button.draw(screen)

	draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT+LOWER_MARGIN-90)
	draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT+LOWER_MARGIN-60)

	# draw tile panel and tiles
	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

 	# choose a tile
	button_count = 0
	for button_count, b in enumerate(button_list):
		if b.draw(screen):
			current_tile = button_count

	# hghlight the selected tile
	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)


	# scroll the map
	if scroll_left and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right and scroll < (MAX_COLS*TILE_SIZE):
		scroll += 5 * scroll_speed

	# add new tiles to the screen
	# get mouse position
	pos = pygame.mouse.get_pos()
	x = (pos[0]+scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	# check that the coordinates are within thetile area
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		# left click to update tile value
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		# right click to reset world data
		if pygame.mouse.get_pressed()[2] == 1:
				world_data[y][x] = -1
	print(x, y)


	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			run = False
		# keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
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
