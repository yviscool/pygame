import pgzrun

WIDTH = 300
HEIGHT = 300

bg = (255, 255, 200)
grid = (50, 50, 50)
green = (0, 255, 0)
red = (255, 0, 0)

markers = []
tile_size = 100
player = 1
winner = 0
game_over = False


# 初始化标记
def init_makers():
	for i in range(3):
		col = [0] * 3
		markers.append(col)


# 绘制背景
def draw_bg():
	screen.fill(bg)


# 绘制线条
def draw_grid():
	for x in range(1, 3):
		# 1 2
		# x
		# (0, 100)  (300, 100)
		# (0, 200)  (300, 200)
		# y
		# (100, 0)  (100, 300)
		# (200, 0)  (200, 300)
		screen.draw.line((0, x*tile_size), (WIDTH, x*tile_size), grid)
		screen.draw.line((x*tile_size, 0), (x*tile_size, HEIGHT), grid)

# 绘制标记 打勾 打叉
def draw_markers():
	# [
	# 	[-1,0,1],
	# 	[1,-1,0],
	# 	[0,0,0],
	# ]
	for i in range(len(markers)):
		col = markers[i]
		# i = 0  [-1, 0, 1]
		# i = 1  [1, -1, 0]
		for j in range(len(col)):
			y = col[j]
			# -1
			if y == -1:
				# print(i, j)
				screen.draw.line((i*tile_size+15, j*tile_size+15), (i*tile_size+85, j*tile_size+85), green)
				screen.draw.line((i*tile_size+15, j*tile_size+85), (i*tile_size+85, j*tile_size+15), green)
			if y == 1:
				screen.draw.circle((i*tile_size+50, j*tile_size+50) , 30, red)


# 检查玩家胜利
def check_winner():

	global winner, game_over

	# 玩家获胜
	for i in range(len(markers)):

		col = markers[i]

		# 玩家获胜规则
		player_victor_rule_list = [
			sum(col),
			markers[0][i] + markers[1][i] + markers[2][i],
			markers[0][0] + markers[1][1] + markers[2][2],
			markers[0][2] + markers[1][1] + markers[2][0],
		]

		if 3 in player_victor_rule_list:
			winner = 1
			game_over = True

		if -3 in player_victor_rule_list:
			winner = -1
			game_over = True


		# if sum(col) == 3:
		# 	winner = 1
		# 	game_over = True

		# if markers[0][i] + markers[1][i] + markers[2][i] == 3:
		# 	winner = 1
		# 	game_over = True

		# if markers[0][0] + markers[1][1] + markers[2][2] == 3 or markers[0][2] + markers[1][1] + markers[2][0] == 3:
		# 	winner = 1
		# 	game_over = True

		# if sum(col) == -3:
		# 	winner = -1
		# 	game_over = True

		# if markers[0][i] + markers[1][i] + markers[2][i] == -3:
		# 	winner = -1
		# 	game_over = True


		# if markers[0][0] + markers[1][1] + markers[2][2] == -3 or markers[0][2] + markers[1][1] + markers[2][0] == -3:
		# 	winner = -1
		# 	game_over = True

	# 平局判断
	inclue_zero = False

	for i in markers:
		if 0 in i:
			inclue_zero = True

	# if 0 in sum(markers, []):
	# 		inclue_zero = True


	if not inclue_zero  and not game_over :
		game_over = True
		winner = 2

	if game_over:
		if winner in [-1, 1]:
			screen.draw.textbox("player " + str(winner) + "  win!", (WIDTH//2-50, HEIGHT//2-60, 100, 100), color=(255, 255, 255), background="green", sysfontname="宋体")
		else:
			screen.draw.textbox("player tie!", (WIDTH//2-50, HEIGHT//2-60, 100, 100), color=(255, 255, 255), background="green", sysfontname="宋体")

# 初始化标记数组
init_makers()


def draw():
	# 绘制背景
	draw_bg()
	# 绘制横竖线
	draw_grid()
	# 绘制标记
	draw_markers()
	# 检查玩家胜利
	check_winner()



def update():
	pass

def on_mouse_down(pos):
	pass

def on_mouse_up(pos):
	global  player

	cell_x, cell_y = pos


	if not game_over:
		x = cell_x // 100
		y = cell_y // 100

		if markers[x][y] == 0:
			markers[x][y] = player
			player *= -1




pgzrun.go()
