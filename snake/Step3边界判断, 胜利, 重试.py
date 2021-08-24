import pygame
import random
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
food = [0,0]
new_food = True
new_piece = [0,0]
score = 0
game_over = False
clicked = False
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
food_col = (200, 50, 50)
blue = (0,0, 255)

# 长方形 for play again
again_rect = Rect(screen_width//2-80, screen_height//2, 160, 50)

font = pygame.font.SysFont(None, 40)

def draw_screen():
	screen.fill(bg)

def draw_score():
	score_text = 'Score: ' + str(score)
	score_img = font.render(score_text, True, blue)
	screen.blit(score_img, (0, 0))

def check_game_over(game_over):

	# 检查蛇是否吃掉了自己
	# 跳过自己头部
	for segment in snake_pos[1:]:
		if snake_pos[0] == segment:
			game_over = True

	# 检查蛇是否超出了屏幕

	if snake_pos[0][0] < 0 or snake_pos[0][0] > screen_width or snake_pos[0][1] < 0 or snake_pos[0][1] > screen_height:
		game_over = True

	return game_over

def draw_game_over():
	over_text = 'Game Over!'
	over_img = font.render(over_text, True, blue)
	pygame.draw.rect(screen,red, (screen_width//2-80, screen_height//2-60, 160, 50))
	screen.blit(over_img, (screen_width//2-80, screen_height//2-50))

	again_text = 'Play Again?'
	again_img = font.render(again_text, True, blue)
	pygame.draw.rect(screen, red, again_rect)
	screen.blit(again_img, (screen_width//2-80, screen_height//2+10))


run = True

while run:

	# 画出背景颜色
	draw_screen()

	# 绘制分数
	draw_score()


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

	# 创建食物
	if new_food == True:
		new_food = False
		food[0] = cell_size * random.randint(0, screen_width/cell_size -1)
		food[1] = cell_size * random.randint(0, screen_height/cell_size -1)

	# 绘制食物
	pygame.draw.rect(screen, food_col, (food[0], food[1] ,cell_size , cell_size))

	# 检查食物和蛇之间的碰撞
	if snake_pos[0] == food:
		new_food = True
		new_piece = list(snake_pos[-1])
		if direction == 1:
			new_piece[1] += cell_size
		if direction == 3:
			new_piece[1] -= cell_size
		if direction == 2:
			new_piece[0] -= cell_size
		if direction == 4:
			new_piece[0] += cell_size

		snake_pos.append(new_piece)

		score += 1

	if game_over == False:

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
			game_over = check_game_over(game_over)

	if game_over == True:
		draw_game_over()

		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
		if event.type == pygame.MOUSEBUTTONUP and clicked == True:
			clicked = False
			pos = pygame.mouse.get_pos()
			if again_rect.collidepoint(pos):
				direction = 1 # 1 is up 2 is right 3down 4 left
				update_snake = 0
				food = [0,0]
				new_food = True
				new_piece = [0,0]
				score = 0
				game_over = False
				# 蛇
				snake_pos = [ [int(screen_width/2), int(screen_height/2)]]
				snake_pos.append( [int(screen_width/2), int(screen_height/2)+cell_size] )
				snake_pos.append( [int(screen_width/2), int(screen_height/2)+cell_size*2] )
				snake_pos.append( [int(screen_width/2), int(screen_height/2)+cell_size*3] )



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
