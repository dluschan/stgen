from .common import *


class Type2(Task01):
	"""Решение неравенств в различных системах счисления."""
	def __init__(self):
		super().__init__()
		self.base, self.degree = self.linked()
		self.question = 'Определите количество целых решений неравенства {inequality}.'
		self.distance = randint(1, 1000)
		left = transform(self.number, self.base, based=True)
		right = transform(self.number + self.distance + 1, self.base ** self.degree, based=True)
		self.left_sign = randint(0, 1)
		self.right_sign = randint(0, 1)
		letter = 'αβγδεζηθικλμνξοπρστυφχψω'
		signs = [' \lt ', ' \leqslant ']
		self.inequality = self.latex(left + signs[self.left_sign] + choice(letter) + signs[self.right_sign] + right)

	def category(self):
		return super().category() + 'Тип 2'

	def question_text(self):
		return self.question.format(inequality=self.inequality)

	def question_answer(self):
		return self.distance + self.left_sign + self.right_sign

