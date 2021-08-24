import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

# 游戏变量
cell_size = 10
direction = 1 # 1 is up 2 is right 3down 4 left
update_snake = 0

# 蛇
snake_pos = [ [int(screen_width/2), int(screen_height/2)]]
snake_pos.append( [int(screen_width/2), int(screen_height/2)+cell_size] )
snake_pos.append( [int(screen_width/2), int(screen_height/2)+cell_size*2] )
snake_pos.append( [int(screen_width/2), int(screen_height/2)+cell_size*3] )


# 定义颜色
bg = (255, 200, 150)
red = (255, 5, 5)

body_inner = (50, 175, 25)
body_outer = (100, 100, 200)



def draw_screen():
	screen.fill(bg)


run = True

while run:

	# 画出背景颜色
	draw_screen()





	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and direction != 3:
				direction = 1
			if event.key == pygame.K_RIGHT and direction != 4:
				direction = 2
			if event.key == pygame.K_DOWN and direction != 1:
				direction = 3
			if event.key == pygame.K_LEFT and direction != 2:
				direction = 4

	if update_snake > 90:

		update_snake = 0
		#  [1,2,3,4] =. [4,1,2,3]
		# 只要把最后一个格子调到头部的话, 其他都不用动保持原状
		snake_pos = snake_pos[-1:] + snake_pos[:-1]
		# up
		if direction == 1:
			snake_pos[0][0] = snake_pos[1][0]
			snake_pos[0][1] = snake_pos[1][1] - cell_size
		# down
		if direction == 3:
			snake_pos[0][0] = snake_pos[1][0]
			snake_pos[0][1] = snake_pos[1][1] + cell_size
		# right
		if direction == 2:
			snake_pos[0][1] = snake_pos[1][1]
			snake_pos[0][0] = snake_pos[1][0] + cell_size
		# left
		if direction == 4:
			snake_pos[0][1] = snake_pos[1][1]
			snake_pos[0][0] = snake_pos[1][0] - cell_size

	head = 1
	# 绘制蛇
	for x in snake_pos:
		if head == 0:
			pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
			pygame.draw.rect(screen, body_inner, (x[0]+1, x[1]+1, cell_size-2, cell_size-2))
		if head == 1:
			pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
			pygame.draw.rect(screen, red, (x[0]+1, x[1]+1, cell_size-2, cell_size-2))
			head = 0

	pygame.display.update()

	update_snake += 1

pygame.quit()
