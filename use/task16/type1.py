from .common import *
from ..tools.decompose import *


class Type1(Task16):
	'''Поиск системы счисления выражения.'''
	def __init__(self):
		super().__init__()
		self.base = choice(list(range(3, 37)))
		self.letter = choice('αβγδεζηθικλμνξοπρστυφχψω')
		self.question = 'Определите систему счисления {letter}, в которой верно тождество {equation}.'

	def category(self):
		return super().category() + 'Тип 1'

	def question_text(self):
		return self.question.format(letter=self.latex(self.letter), equation=self.latex(self.equation))

	def question_answer(self):
		return self.base


class SubtypeA(Type1):
	'''Определение системы счисления чисел с помощью линейного уравнения.'''
	def __init__(self):
		super().__init__()
		k = choice(list(range(-5, -1)) + list(range(1, 5)))
		b = -k * self.base
		num = decompose([k, b], self.base - 1)
		left = ' + '.join(map(lambda x, y: self.digits[x] + self.digits[y] + '_{' + self.letter + '}', num[0][0], num[1][0]))
		right = ' + '.join(map(lambda x, y: self.digits[x] + self.digits[y] + '_{' + self.letter + '}', num[0][1], num[1][1]))
		self.equation = ' = '.join([left, right])

	def category(self):
		return super().category() + 'Подтип A'


class SubtypeB(Type1):
	'''Определение системы счисления чисел с помощью линейного уравнения.'''
	def __init__(self):
		super().__init__()
		a = choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
		a = choice([-5, -4, -3, -2, -1, 0, 1])
		b = -a*(self.base + x_2)
		c = a * self.base * x_2
		num = decompose([a, b, c], self.base - 1)
		left = ' + '.join(map(lambda x, y, z: self.digits[x] + self.digits[y] + self.digits[z] + '_{' + self.letter + '}', num[0][0], num[1][0], num[2][0]))
		right = ' + '.join(map(lambda x, y, z: self.digits[x] + self.digits[y] + self.digits[z] + '_{' + self.letter + '}', num[0][1], num[1][1], num[2][0]))
		self.equation = ' = '.join([left, right])

	def category(self):
		return super().category() + 'Подтип B'
