from itertools import product
from random import shuffle, randint, randrange
from ..tools.common import letters

class Field:
	"""
	Поле для робота - двумерный массив ячеек.

	Число в массиве - признак стен. Оно черырёхбитное. Каждый бит указывает на наличие стены в определённом направлении: младший - наверх, следующий - влево и т.д.

	Пример ячейки: 6 = 0110 => эту клетку стены окружают слева и снизу.
	Пример пустого поля 6x6, окружённого стенами.
	t = [
		[3, 1, 1, 1, 1, 9],
		[2, 0, 0, 0, 0, 8],
		[2, 0, 0, 0, 0, 8],
		[2, 0, 0, 0, 0, 8],
		[2, 0, 0, 0, 0, 8],
		[6, 4, 4, 4, 4, 12],
	]
	"""
	def __init__(self, r, c = None, hw = None, vw = None, closed = True):
		self.goal = None
		self.rows = r
		if c is None:
			c = r
		self.cols = c
		assert self.cols <= len(letters)
		self.letters = letters.upper()[:self.cols]
		self.t = [[0] * self.cols for _ in range(self.rows)]
		self.hw = hw or []
		self.vw = vw or []
		self.hor_placing_wall()
		self.ver_placing_wall()
		if closed:
			self.placing_wall_around()

	def __rep__(self):
		"""Представление лабиринта в виде матрицы 16-ричных чисел без разделителей"""
		return '\n'.join(''.join(map(lambda x: hex(x)[2], row)) for row in self.t)

	def __str__(self):
		return self.get_svg()

	def set_goal(self, goal):
		self.goal = goal

	def get_svg(self):
		"""Представление лабиринта в виде svg картинки"""
		indent = 50
		digit_width = 100
		cell_width = 100
		cell_height = 100
		font_size = 50
		grid_width = self.cols * cell_width
		grid_height = self.rows * cell_height
		svg = f"""<svg width="50%" max-width="400px" viewBox="0 0 {indent + digit_width + grid_width + indent} {indent + grid_height + cell_height + indent}"\n"""
		grid = """<g stroke="black" stroke-width="2">\n"""
		for i in range(self.rows + 1):
			grid += f"""<line x1="{indent + digit_width}" y1= "{indent + i*cell_height}" x2="{indent + digit_width + grid_width}" y2= "{indent + i*cell_height}" />\n"""
		for i in range(self.cols + 1):
			grid += f"""<line x1="{indent + digit_width + i*cell_width}" y1= "{indent}" x2="{indent + digit_width + i*cell_width}" y2= "{indent + grid_height}" />\n"""
		grid += """</g>\n"""
		if self.goal:
			goal = f"""<rect x="{indent + digit_width + self.goal[1] * cell_width}" y="{indent + self.goal[0] * cell_height}" width="{cell_width}" height="{cell_height}" fill="silver" stroke="black" stroke-width="2" />\n"""
		else:
			goal = "\n"
		digits = ""
		for r in range(1, self.rows + 1):
			digits += f"""<text text-anchor="middle" x="{indent + digit_width / 2}" y="{indent + cell_height * (r - 1) + cell_height / 2 + font_size / 2}" font-size="{font_size}px">{r}</text>\n"""
		letters = ""
		for i, c in enumerate(self.letters, 1):
			digits += f"""<text text-anchor="middle" x="{indent + digit_width + cell_width * (i - 1) + cell_width / 2}" y="{indent + grid_height + indent / 2 + font_size / 2}" font-size="{font_size}px">{c}</text>\n"""
		walls = """<g stroke="black" stroke-width="7">\n"""
		walls += f"""<rect x="{indent + digit_width}" y="{indent}" width="{grid_width}" height="{grid_height}" fill="None" />"""
		for c, r in self.hw:
			walls += f"""<line x1="{indent + digit_width + cell_width * c}" y1="{indent + cell_height * (r + 1)}" x2="{indent + digit_width + cell_width * (c + 1)}" y2="{indent + cell_height * (r + 1)}" />\n"""
		for r, c in self.vw:
			walls += f"""<line x1="{indent + digit_width + cell_width * (c + 1)}" y1="{indent + cell_height * r}" x2="{indent + digit_width + cell_width * (c + 1)}" y2="{indent + cell_height * (r + 1)}" />\n"""
		walls += """</g>\n"""
		svg_end = """</svg>"""
		return svg + grid + goal + digits + letters + walls + svg_end

	def hor_placing_wall(self):
		for c, r in self.hw:
			self.t[r][c] |= 4
			self.t[r+1][c] |= 1

	def ver_placing_wall(self):
		for r, c in self.vw:
			self.t[r][c] |= 8
			self.t[r][c+1] |= 2

	def placing_wall_around(self):
		for r, c in product([0], range(self.cols)):
			self.t[r][c] |= 1
		for r, c in product(range(self.cols), [0]):
			self.t[r][c] |= 2
		for r, c in product([-1], range(self.cols)):
			self.t[r][c] |= 4
		for r, c in product(range(self.cols), [-1]):
			self.t[r][c] |= 8

	def fu(self, pos):
		assert 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols, pos
		return self.t[pos[0]][pos[1]] & 1 == 0

	def fl(self, pos):
		assert 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols, pos
		return self.t[pos[0]][pos[1]] & 2 == 0

	def fd(self, pos):
		assert 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols, pos
		return self.t[pos[0]][pos[1]] & 4 == 0

	def fr(self, pos):
		assert 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols, pos
		return self.t[pos[0]][pos[1]] & 8 == 0


class Robot:
	"""Робот, который ходит по лабиринту"""
	def up(self):
		assert self.free_up()
		self.pos[0] -= 1

	def left(self):
		assert self.free_left()
		self.pos[1] -= 1

	def down(self):
		assert self.free_down()
		self.pos[0] += 1

	def right(self):
		assert self.free_right()
		self.pos[1] += 1

	def free_up(self):
		return self.field.fu(self.pos)

	def free_left(self):
		return self.field.fl(self.pos)

	def free_down(self):
		return self.field.fd(self.pos)

	def free_right(self):
		return self.field.fr(self.pos)


class CornerRobot(Robot):
	"""
	Робот, который хочет дойти в угол поля.
	
	Угол - двухбитовое число. Младший бит - горизонталь: 0 - левый, 1 - правый; старший бит - вертикаль: 0 - верхний, 1 - нижний.
	"""
	class Algorithm:
		def __init__(self, movies):
			self.movies = movies
			shuffle(self.movies)
			opt = randint(0, 2), randint(0, 2)
			self.code = f"while free_{self.movies[0]}() or free_{self.movies[1]}():\n"
			for i in range(2):
				if opt[i] == 0: # смелость и отвага
					self.code += f"""    {self.movies[i]}()\n"""
				elif opt[i] == 1: # робкий шаг
					self.code += f"""    if free_{self.movies[i]}():\n"""
					self.code += f"""        {self.movies[i]}()\n"""
				else: # вперёд!
					self.code += f"""    while free_{self.movies[i]}():\n"""
					self.code += f"""        {self.movies[i]}()\n"""

		def __str__(self):
			return self.code

	def __init__(self, field, corner):
		steps = [
			["left", "right"],
			["up"  , "down"]
		]

		self.field = field
		self.goal = [(self.field.rows - corner // 2) % self.field.rows, (self.field.cols - corner % 2) % self.field.cols]
		self.cell = self.field.letters[self.goal[1]] + str(self.goal[0] + 1)
		self.field.set_goal(self.goal)
		self.hor = steps[0][corner % 2]
		self.ver = steps[1][corner // 2]
		self.algo = CornerRobot.Algorithm([self.hor, self.ver])

	def count(self):
		res = 0
		for x, y in product(range(self.field.rows), range(self.field.cols)):
			self.pos = [x, y]
			try:
				up = self.up
				left = self.left
				down = self.down
				right = self.right
				free_up = self.free_up
				free_left = self.free_left
				free_down = self.free_down
				free_right = self.free_right
				exec(self.algo.code)
			except AssertionError:
				continue
			if self.pos == self.goal:
				res += 1
		return res


class CircleRobot(Robot):
	"""
	Робот, который ходит по кругу.
	
	Поведение - двухбитовое число. Младший бит - направление проверки: 0 - вперёд, 1 - вбок; старший бит - направление круга: 0 - против часовой стрелки, 1 - по часовой стрелке.
	"""
	class Algorithm:
		def __init__(self, mode):
			self.movies = ['up', 'left', 'down', 'right']
			if mode // 2:
				self.movies = self.movies[::-1]
			# случайное смещение движений
			k = randrange(4)
			self.movies = self.movies[k:] + self.movies[:k]
			self.look = ["free_" + m for m in self.movies]
			# смещаем направление взгляда на один такт
			if mode % 2:
				k = 3
				self.look = self.look[k:] + self.look[:k]

			self.code = ""
			for check, go in zip(self.look, self.movies):
				self.code += f"""while {check}():\n"""
				self.code += f"""    {go}()\n"""

		def __str__(self):
			return self.code

	def __init__(self, field):
		self.field = field
		self.algo = CircleRobot.Algorithm(randrange(4))

	def count(self):
		res = 0
		for x, y in product(range(self.field.rows), range(self.field.cols)):
			self.pos = [x, y]
			try:
				up = self.up
				left = self.left
				down = self.down
				right = self.right
				free_up = self.free_up
				free_left = self.free_left
				free_down = self.free_down
				free_right = self.free_right
				exec(self.algo.code)
			except AssertionError:
				continue
			if self.pos == [x, y]:
				res += 1
		return res


