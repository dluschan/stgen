from .common import *
from ..tools.decompose import *


class Type0(Task16):
	"""Поиск системы счисления числа."""
	def __init__(self):
		super().__init__()
		self.question = 'Запись числа {number} в некоторой системе счисления выглядит как {view}. Найдите основание этой системы счисления.'

	def category(self):
		return super().category() + 'Тип 0/'

	def question_text(self):
		return self.question.format(number=self.latex(self.number), view=self.latex(transform(self.number, self.base)))

	def question_answer(self):
		return self.base


class SubtypeA(Type0):
	"""Решение линейных уравнений в различных системах счисления."""
	def __init__(self):
		super().__init__()
		self.number = randint(self.base, self.base ** 2 - 1)

	def category(self):
		return super().category() + 'Подтип A'


class SubtypeB(Type0):
	"""Решение квадратных уравнений в различных системах счисления."""
	def __init__(self):
		super().__init__()
		self.number = randint(self.base ** 2, self.base ** 3 - 1)

	def category(self):
		return super().category() + 'Подтип B'
