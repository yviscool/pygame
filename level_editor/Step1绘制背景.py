import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH+SIDE_MARGIN, SCREEN_HEIGHT+LOWER_MARGIN))
pygame.display.set_caption('Level Editor')


# define game variables
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

#load images
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

# create function for drawing background
def draw_bg():

	screen.blit(sky_img, (0, 0))
	screen.blit(mountain_img, (0, SCREEN_HEIGHT- mountain_img.get_height() - 300))
	screen.blit(pine1_img, (0, SCREEN_HEIGHT- pine1_img.get_height() - 150))
	screen.blit(pine2_img, (0, SCREEN_HEIGHT- pine2_img.get_height() ))

run = True

while run:

	draw_bg()



	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			run = False


	pygame.display.update()


pygame.quit()
