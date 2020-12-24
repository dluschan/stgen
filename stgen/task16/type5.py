from .common import *
from math import log
from random import sample


class Type5(Task16):
	"""Составление минимальных и максимальных чисел в разных системах счисления с дополнительными условиями."""
	def __init__(self):
		super().__init__()
		self.question = """Определите {extrem} {width} число {baseTarget}, запись которого {baseLimit} содержит 
		ровно {repeats} {digit}. В ответ запишите искомое число {baseTarget}."""
		self.limit = 10
		self.base = randint(2, 6)
		self.degreeTarget, self.degreeLimit = sample(range(1, int(log(36, self.base)) + 1), 2)
		self.repeats = randint(1, self.limit // self.degreeLimit)
		self.digit = randint(0, self.base ** self.degreeLimit - 1)
		base_width = (self.repeats - 1) * self.degreeLimit + len(transform(self.digit, self.base))
		if not self.digit:
			base_width += self.degreeLimit
		min_width = (base_width + self.degreeTarget - 1) // self.degreeTarget
		self.width = randint(min_width, min_width + 3)

	def category(self):
		return super().category() + 'Тип 5/'

	def sign(self, n):
		assert(0 < n < 21)
		return self.order[n] + self.sign_suffix

	def question_text(self):
		return self.question.format(
			extrem=self.extrem,
			width=self.sign(self.width),
			baseTarget=self.notation(self.base ** self.degreeTarget),
			baseLimit=self.notation(self.base ** self.degreeLimit),
			repeats=self.latex(self.repeats) + ' ' + self.digits_word(self.repeats),
			digit=self.latex(self.digits[self.digit])
		)

	def question_answer(self):
		return transform(self.number, self.base ** self.degreeTarget, self.digits)


class SubtypeA(Type5):
	"""Минимальное n-значное число, которое содержит заданное количество цифр."""
	def __init__(self):
		super().__init__()
		self.extrem = 'минимальное'
		self.number = minLimitedNumber(self.base, self.degreeTarget, self.width, self.degreeLimit, self.digit, self.repeats)

	def category(self):
		return super().category() + 'Подтип A'


class SubtypeB(Type5):
	"""Максимальное n-значное число, которое содержит заданное количество цифр."""
	def __init__(self):
		super().__init__()
		self.extrem = 'максимальное'
		self.number = maxLimitedNumber(self.base, self.degreeTarget, self.width, self.degreeLimit, self.digit, self.repeats)

	def category(self):
		return super().category() + 'Подтип B'

