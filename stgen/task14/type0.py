from random import randrange, randint, choice
from .common import Task14
from ..tools.maze import Field, CornerRobot, CircleRobot


class Type0(Task14):
	"""Исполнитель робот."""
	def __init__(self):
		super().__init__()
		self.question = """<p>Сколько клеток лабиринта соответствуют требованию, что, начав движение в ней и выполнив предложенную программу, <var>Робот</var> уцелеет{suffix}?</p>
<div style="float: left; width: 50%">
<h4>Программа:</h4>
<p><pre><code>{algo}</code></pre></p>
</div>
<div>
<h4>Лабиринт:</h4>
{field}
</div>
"""
		self.size = 6, 6
		m = 2 * self.size[0] * self.size[1] - self.size[0] - self.size[1]
		walls = [(randrange(self.size[0]), randrange(self.size[1] - 1)) for _ in range(randint(m // 8, m // 3))]
		k = randint(len(walls) // 3, 2 * len(walls) // 3)
		hor_walls = walls[:k]
		ver_walls = walls[k:]
		self.field = Field(*self.size, hor_walls, ver_walls, True)

	def category(self):
		return super().category() + 'Тип 0/'

	def question_text(self):
		return self.question.format(suffix=self.suffix, field=self.field, algo=self.robot.algo)

	def question_answer(self):
		return self.robot.count()


class SubtypeA(Type0):
	"""Робот идёт в угол."""
	def __init__(self):
		super().__init__()
		self.robot = CornerRobot(self.field, randrange(4))
		self.suffix = f""" и остановится в закрашенной клетке <kbd>{self.robot.cell}</kbd>"""

	def category(self):
		return super().category() + 'Подтип A'


class SubtypeB(Type0):
	"""Робот идёт по кругу."""
	def __init__(self):
		super().__init__()
		self.robot = CircleRobot(self.field)
		self.suffix = f""" и остановится в той же клетке, с которой он начал движение"""

	def category(self):
		return super().category() + 'Подтип B'

