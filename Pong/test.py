import pygame

pygame.init()

screen_width = 600
screen_height = 600


screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('TieTacToe')

run = True

line_width = 6

markers  = []
bg = (255, 255, 200)

l = 200
clicked = False
player = 1

def draw_grid():
	grid = (50, 50, 50)
	for x in range(1,3):
		# 画 x
		pygame.draw.line(screen, grid, (0, x *l), (screen_width, x *l), 6)
		# 画 y
		pygame.draw.line(screen, grid, (x* l, 0), (x * l, screen_width), 6)

def draw_makers():

	# [
	# 	[1, 0, 0],
	# 	[0, -1, 0],
	# 	[0, 1, 0],
	# ]
	grid = (50, 50, 50)

	x_pos = 0
	for x in markers:

		y_pos = 0
		for y in x:


			if y == 1:
				pygame.draw.line(screen, grid, (x_pos*l + 20, y_pos *l +20), (x_pos*l + 180, y_pos *l +180), 6)
				pygame.draw.line(screen, grid, (x_pos*l + 180, y_pos *l +20), (x_pos*l+20,  y_pos *l + 180), 6)
			if y == -1:
				pygame.draw.circle(screen, grid, (x_pos * l + l/2, (y_pos+1) * l - l/2), l/2)

			y_pos += 1


		x_pos += 1

for x in range(3):
	row = [0] * 3
	markers.append(row)



while run:

	screen.fill(bg)
	draw_grid()
	draw_makers()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
		if event.type == pygame.MOUSEBUTTONUP and clicked == True:
			clicked = False
			cell_x, cell_y = pygame.mouse.get_pos()
			print(markers)
			print('....')
			if markers[cell_x//l][cell_y//l] == 0:
				markers[cell_x//l][cell_y//l] = player
				player *= -1
			print(markers)


	pygame.display.update()

pygame.quit()
