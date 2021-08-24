import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Pong')


# 字体
font = pygame.font.SysFont('Constantla', 30)

#  游戏变量
margin = 50
cpu_score = 0
palyer_score = 0


# 颜色
bg = (50, 25, 50)
white = (255, 255, 255)

def draw_board():
	screen.fill(bg)
	pygame.draw.line(screen, white, (0, margin), (screen_width, margin))

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

run = True

while run:

	draw_board()
	draw_text('CPU: ' + str(cpu_score), font, white, 20, 15)
	draw_text('P1: ' + str(palyer_score), font, white, screen_width-100, 15)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()

