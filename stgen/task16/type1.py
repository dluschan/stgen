from .common import *
from ..tools.decompose import *


class Type1(Task16):
	"""Поиск системы счисления выражения."""
	def __init__(self):
		super().__init__()
		self.base = choice(list(range(3, 37)))
		self.letter = choice('αβγδεζηθικλμνξοπρστυφχψω')
		self.question = 'Определите систему счисления {letter}, в которой верно тождество {equation}.'

	def category(self):
		return super().category() + 'Тип 1/'

	def question_text(self):
		return self.question.format(letter=self.latex(self.letter), equation=self.latex(self.equation))

	def question_answer(self):
		return self.base


class SubtypeA(Type1):
	"""Определение системы счисления чисел с помощью линейного уравнения."""
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
	"""Определение системы счисления чисел с помощью квадратного уравнения."""
	def __init__(self):
		super().__init__()
		# -a(x1+x2)=b
		# - ax1 - ax2 = b
		# - x1 - x2 > 0
		# при x2 < -x1 : b > 0
		# - ax1 - ax2 < k * (x1 - 1)
		# x2 > - x1 - k * (x1 - 1) / a
		#
		# при x2 > -x1: b < 0
		# ax1 + ax2 < k * (x1 - 1)
		# x2 < - x1 + k * (x1 - 1) / a
		#
		# - x1 * a - k * (x1 - 1) < x2 * a < - x1 * a + k * (x1 - 1)
		#
		# c = a*x1*x2
		# при x2 > 0
		# a * x1 * x2 < k * (x1 - 1)
		# x2 < k * (x1 - 1) / (a * x1)
		#
		# при x2 < 0
		# - a * x1 * x2 < k * (x1 - 1)
		# x2 > - k * (x1 - 1) / (a * x1)
		#
		# - k * (x1 - 1) / x1 < x2*a < k * (x1 - 1) / x1
		#
		# - x1 * a + k * x1 - k > - k + k / x1
		# - x1 * a + k * x1 > k / x1
		# x1 * (k - a) > k / x1
		# x1^2 * k - x1^2 * a > k
		# x1^2 * k - k > x1^2 * a
		# k * (x1^2 - 1) > x1^2 * a
		# k > x1^2 * a / (x1^2 - 1)
		#
		# x2 = p / q

		a = choice(list(range(1, 6)))
		k = int(self.base ** 2 * a / (self.base ** 2 - 1) + 1)
		l1 = - self.base * a - k * (self.base - 1)
		r1 = - self.base * a + k * (self.base - 1)
		l2 = - k * (self.base - 1) / self.base
		r2 = k * (self.base - 1) / self.base
		x2_q = [x2 for x2 in range(int(max(l1, l2) - 1), int(min(r1, r2) + 1)) if l1 <= x2 <= r1 and l2 <= x2 <= r2]
		log = "x1 = {x1}, a = {a}, k = {k}, l1 = {l1}, r1 = {r1}, l2 = {l2}, r2 = {r2}, x2 = {x2}".format(
			x1=self.base, a=a, l1=l1, r1=r1, l2=l2, r2=r2, x2=x2_q, k=k
		)
		assert x2_q, log
		p = choice(x2_q)
		b = - a * self.base - p
		c = self.base * p
		log += ", p = {p}, b = {b}, c = {c}".format(p=p, b=b, c=c)
		assert abs(a) <= k * (self.base - 1), log
		assert abs(b) <= k * (self.base - 1), log
		assert abs(c) <= k * (self.base - 1), log
		num = signed_decompose([a, b, c], self.base - 1)
		left = ' + '.join(map(lambda x, y, z: self.digits[x] + self.digits[y] + self.digits[z] + '_{' + self.letter + '}', num[0][0], num[1][0], num[2][0]))
		right = ' + '.join(map(lambda x, y, z: self.digits[x] + self.digits[y] + self.digits[z] + '_{' + self.letter + '}', num[0][1], num[1][1], num[2][1]))
		self.equation = ' = '.join([left, right])

	def category(self):
		return super().category() + 'Подтип B'
