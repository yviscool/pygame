import pygame
import random

# 初始化
pygame.init()

# 时钟
clock = pygame.time.Clock()

# 音乐
shot_fx = pygame.mixer.Sound('sound1.mp3')
raw_array = shot_fx.get_raw()

# 音乐裁剪
raw_array = raw_array[600000:800000]
# raw_array = raw_array[0:2000000]
shot_fx = pygame.mixer.Sound(buffer=raw_array)
shot_fx.set_volume(0.5)

# 游戏帧数
FPS = 60
# 游戏屏幕宽度, 高度
WIDTH  = 640
HEIGHT = 900

# 创建屏幕对象
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 游戏执行条件
run = True
# 游戏结束  0 进行  1 胜利  -1 失败
game_over = 0

# 常量
BORDER = 1

# 颜色
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (51, 51, 51)
WHITE_GREY = (204, 204, 204)
GOLD = (255, 255, 0)


BLOCKS_TYPE_FAILURE = -1
BLOCKS_TYPE_COMMON = 0
BLOCKS_TYPE_CLICKABLE = 1
BLOCKS_TYPE_CLICKED = 2
BLOCKS_TYPE_GOLD = 3
BLOCKS_TYPE_START = 4
# -1 代表红色(失败)
# 0 代表白色(不可点击-否则失败)\
# 1 代表灰色(可点击)
# 2 代表白灰色(被点击的后的)
# 3 代表黄色 (游戏开始的最后一排)
# 4 代表开始的色块
markers = [
	[0, 0, 0, 0, 3],
	[0, 0, 0, 0, 3],
	[0, 0, 0, 0, 3],
	[0, 0, 0, 0, 3],
]

# [
# 	[经典,街机(竞技)],
# 	[禅,极速],
# 	[接力,排行榜],
# ]
# 开始菜单选择按钮
select_markers = [
	[1, 4],
	[2, 5],
	[3, 6]
]

# 微软雅黑粗体 44 大小
yahei44 = pygame.font.SysFont('microsoftjhengheiui', 44, bold=True)
yahei50 = pygame.font.SysFont('microsoftjhengheiui', 50)
yahei60_bold = pygame.font.SysFont('microsoftjhengheiui', 60, bold=True)

# print(pygame.font.get_fonts())

# 绘制文字
def draw_text(text, font, text_col, x, y, is_center=False):
	img = font.render(text, True, text_col)
	if is_center:
		rect = img.get_rect()
		rect.center = (x, y)
		screen.blit(img, rect)
	else:
		screen.blit(img, (x,y))

# 绘制网格布局
def draw_grid():
	for i in range(5):
		pygame.draw.line(screen, BLACK, ( 0,  i*225 ),( WIDTH, i*225), BORDER)
		pygame.draw.line(screen, BLACK, ( i*160, 0 ),( i*160, HEIGHT), BORDER)

# 游戏按钮
class Button:

	def __init__(self, types, x, y, w, h):

		color_lst = [WHITE, BLACK]

		self.types = types
		self.w = w
		self.h = h

		if types == 1:
			self.txt = '经典'
			self.start = 100
		if types == 2:
			self.txt = '禅'
			self.start = 800
		if types == 3:
			self.txt = '接力'
			self.start = 1500
		if types == 4:
			self.txt = '街机(竞技)'
			self.start = 100
		if types == 5:
			self.txt = '极速'
			self.start = 800
		if types == 6:
			self.txt = '排行榜'
			self.start = 1500

		if types in [1,2,3]:
			x = -w
		else:
			x = x * 2

		self.rect = pygame.Rect(x, y, w, h)

		self.block_color = color_lst[ (types-1) % 2 ]
		self.txt_color   = color_lst[ types     % 2 ]

		self.time  = pygame.time.get_ticks()

		self.speed = 10

		if self.types in [1,2,3]:
			self.direction = 1 # 向右
		else:
			self.direction = -1 # 向左

		self.reverse = False # 动画是否反转 , 选择和开始的时候


	def draw(self):

		# 绘制色块
		pygame.draw.rect(screen, self.block_color, self.rect)

		# 绘制文本
		draw_text(
			self.txt,
			yahei60_bold,
			self.txt_color,
			self.rect.x + 160,
			self.rect.y + 150,
			True
		)

	def update(self):

		self.move()
		self.click()

	def move(self):

		global step

		now = pygame.time.get_ticks()

		if self.speed:

			if now - self.time > self.start:

				direction = -1 * self.direction if self.reverse else self.direction

				self.rect.x += self.speed * direction

				if not self.reverse:
					# 向右
					if direction == 1:
						if self.rect.x >= 0:
							self.rect.x = 0
							self.speed  = 0
					# 向左
					if direction == -1:
						if self.rect.x <= 320:
							self.rect.x = 320
							self.speed  = 0
				else:
					# 向右
					if direction == -1:
						if self.rect.x <= -320:
							self.rect.x = -320
							self.speed  = 0
							step = 1
					# 向左
					if direction == 1:
						if self.rect.x >= 640:
							self.rect.x = 640
							self.speed  = 0

	def click(self):

		pos = pygame.mouse.get_pos()

		# 鼠标按下松开的时候
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		# 鼠标左键按下的时候
		if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
			self.clicked = True

			self.time = pygame.time.get_ticks()
			self.speed = 10

			self.reverse = True

			if self.types in [1,4]:
				self.start = 100
			elif self.types in [2, 5]:
				self.start = 500
			else:
				self.start = 800

			if self.rect.x // self.w == pos[0] // self.w \
				and self.rect.y // self.h == pos[1] // self.h:
				print('点击了')


# 游戏色块
class Block:

	def __init__(self, types, x, y):

		self.rect = pygame.Rect(x, y, 160, 225)
		self.txt = None

		self.get_color(types)

		self.move = False

		self.speed = 45
		self.limit = 0

		# 点击的色块
		self.w = 0
		self.h = 0
		self.front_color = None


	def get_color(self, types):
		# -1 代表红色(失败)
		# 0 代表白色(不可点击-否则失败)
		# 1 代表灰色(可点击)   1 => 2
		# 2 代表白灰色(被点击的后的)
		# 3 代表黄色 (游戏开始的最后一排)
		# 4 代表开始的那一块色块
		if types == BLOCKS_TYPE_FAILURE:
			self.color = RED
		elif types == BLOCKS_TYPE_COMMON:
			self.color = WHITE
		elif types == BLOCKS_TYPE_CLICKABLE:
			self.color = GREY
		elif types == BLOCKS_TYPE_CLICKED:
			self.color = GREY
			self.front_color = WHITE_GREY
		elif types == BLOCKS_TYPE_GOLD:
			self.color = GOLD
		elif types == BLOCKS_TYPE_START:
			self.color = GREY
			self.txt = True

	def draw(self, clicked):
		# 绘制色块
		pygame.draw.rect(screen, self.color, self.rect)

		# 正确点击的时候 变成灰白 面积会慢慢变大
		if self.front_color:
			rect = pygame.Rect(0, 0, self.w, self.h)
			rect.center = self.rect.center
			pygame.draw.rect(screen, WHITE_GREY, rect)
			# 增大面积
			self.w += 20
			self.h += 25
			# 越界判断
			if self.w >= 160:
				self.w = 160
			if self.h >= 225:
				self.h = 225

		# 边框
		pygame.draw.rect(screen, BLACK, self.rect, BORDER)

		# 开始按钮
		if not clicked and self.txt:
			draw_text(
				'开始',
				yahei44,
				WHITE,
				self.rect.x + 80,
				self.rect.y + 112,
				True
			)

		if clicked and self.txt:
			self.txt = None

	def update(self):

		if self.move:

			self.rect.y += self.speed

			self.limit += self.speed

			if self.limit >= 225:
				self.move = False
				self.limit = 0

class World:

	def __init__(self):

		self.blocks = []
		self.buttons = []

		# 是否被点击
		self.clicked = False

		# 倒计时
		self.time = None

	# 生成最初砖块
	def init_block(self):
		# 随机产生色块
		# markers = [
		# 	[0, 0, 0, 0, 3],
		# 	[0, 0, 0, 0, 3],
		# 	[0, 0, 0, 0, 3],
		# 	[0, 0, 0, 0, 3],
		# ]
		#   0   1  2  3  4

		W = WIDTH // 4
		H = HEIGHT // 4

		# 会产生四个黑块
		for y in range(4):
			x = random.randint(0, WIDTH) // W
			# 产生开始砖块
			if y == 3:
				markers[x][y] = BLOCKS_TYPE_START
			# 常规可点击砖块
			else:
				markers[x][y] = BLOCKS_TYPE_CLICKABLE

		# 砖块
		for x_i, x in enumerate(markers):

			for y_i, block_type in enumerate(x):

				x_pos = x_i * W
				y_pos = y_i * H

				# 让所有砖块上移一层 所以要减去 H => 225
				block = Block(block_type, x_pos, y_pos-H)

				self.blocks.append(block)


	def init_select_block(self):

		W = WIDTH // 2
		H = HEIGHT // 3

		for y_i, y in enumerate(select_markers):

			for x_i, x in enumerate(y):

				x_pos = x_i * W
				y_pos = y_i * H

				b = Button(x, x_pos, y_pos, W, H)

				self.buttons.append(b)

	def draw(self):

		for block in self.blocks:
			block.draw(self.clicked)

		# 倒计时
		counter = '0.000"'

		if self.time:

			now = pygame.time.get_ticks()

			counter = '{:.3f}'.format(round((now-self.time)/1000, 3)) + '"'

		draw_text(
			counter,
			yahei50,
			RED,
			WIDTH//2,
			50,
			True
		)


	def update(self):

		# 获取鼠标位置
		pos = pygame.mouse.get_pos()

		# 鼠标按下松开的时候
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		# 鼠标左键按下的时候
		if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:

			self.clicked = True

			if not self.time:
				self.time = pygame.time.get_ticks()

			for block in self.blocks:
				# block.update(pos)
				# 判断是否被点击了，是的话 全部都要移动
				if pos[1] // 225 == 2:

					# 判断哪个块是否被点击了
					if block.rect.x // 160  == pos[0] // 160 \
						and block.rect.y // 225 == pos[1] // 225:

						if block.color == GREY:
							shot_fx.play()
							block.get_color(2)
						else:
							block.get_color(-1)

					block.move = True

		for block in self.blocks:

			block.update()

			# 越界判断
			for block in self.blocks:
				if block.rect.y > HEIGHT - 10:
					self.blocks.remove(block)

			# 当最后一排色块被移除时候, 要补充最前面的砖块
			if len(self.blocks) < 20:

				i = random.choice([0, 1, 3, 4])

				for x in range(0, 640, 160):
					# 0 160 320 480
					if x // 100 == i:
						block = Block(BLOCKS_TYPE_CLICKABLE, x, -225)
					else:
						block = Block(BLOCKS_TYPE_COMMON, x, -225)

					self.blocks.append(block)



world = World()

world.init_block()
world.init_select_block()

# 0 选择 1 游戏
step = 0

while run:

	clock.tick(FPS)

	# pygame.draw.line(screen, BLACK, (0, 225), (WIDTH, 225), BORDER)
	# pygame.draw.line(screen, BLACK, (0, 450), (WIDTH, 450), BORDER)
	# pygame.draw.line(screen, BLACK, (0, 675), (WIDTH, 675), BORDER)

	# pygame.draw.line(screen, BLACK, (160, 0), (160, HEIGHT), BORDER)
	# pygame.draw.line(screen, BLACK, (320, 0), (320, HEIGHT), BORDER)
	# pygame.draw.line(screen, BLACK, (480, 0), (480, HEIGHT), BORDER)
	if step == 0:
		screen.fill(BLACK)
	else:
		screen.fill(WHITE)


	if step == 1:
		if game_over == 0:
			world.draw()
			world.update()

	for b in world.buttons:
		b.draw()
		b.update()

	# draw_grid()
	# draw_text(str(round(pygame.time.get_ticks()/10000, 2)), yahei44, RED, WIDTH//2, 50, True)
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				shot_fx.play()

	pygame.display.update()

pygame.quit()