import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

# 游戏变量
cell_size = 10

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



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
