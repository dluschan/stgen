from .common import *
from math import log


class Type5(Task16):
	"""Превод чисел в разные системы счисления."""
	def __init__(self):
		super().__init__()
		self.question = 'Определите наименьшее {sign} {based}, запись которого {base} содержит ровно {repeats} цифр {digit}. В ответ запишите искомое {based}.'
		self.type = 'Тип 5/подтип A'
		self.base = randint(2, 6)
		self.degree = randint(2, int(log(36, self.base)))
		self.repeats = randint(3, 6)
		self.digit = choice(self.digits[1:self.base])
		self.width = randint((self.repeats + self.degree - 1) // self.degree, (self.repeats + self.degree - 1) // self.degree + 3)
		self.number = int(self.digit * self.repeats, self.base)
		if self.number < (self.base ** self.degree) ** (self.width - 1):
			self.number += (self.base ** self.degree) ** (self.width - 1)

	def sign(self, n):
		assert(0 < n < 21)
		return self.signs[n] + self.suffix_sing

	def question_text(self):
		return self.question.format(m = self.latex(self.width), bigbase = self.latex(str(self.base ** self.degree)), base = self.latex(str(self.base)), repeats = self.latex(str(self.repeats)), digit = self.latex(str(self.digit)))

	def question_answer(self):
		return transform(self.number, self.base ** self.degree, self.digits)


class Type5a(Task16):
	"""Превод чисел в разные системы счисления."""
	def __init__(self):
		super().__init__()
		self.question = 'Определите наименьшее число содержащее {m} цифр в системе счисления с основанием {bigbase}, запись которого в системе счисления с основанием {base} содержит ровно {repeats} цифр {digit}. Ответ укажите в системе счисления с основанием {bigbase}.'
		self.type = 'Тип 5/Подтип A'
		self.base = randint(2, 6)
		self.degree = randint(2, int(log(36, 4)))
		self.repeats = randint(3, 8)
		self.digit = choice(self.digits[1:self.base])
		self.width = randint((self.repeats + self.degree - 1) // self.degree, (self.repeats + self.degree - 1) // self.degree + 4)
		self.number = int(self.digit * self.repeats, self.base)
		if self.number < (self.base ** self.degree) ** (self.width - 1):
			self.number += (self.base ** self.degree) ** (self.width - 1)

	def question_text(self):
		return self.question.format(m = self.latex(self.width), bigbase = self.latex(str(self.base ** self.degree)), base = self.latex(str(self.base)), repeats = self.latex(str(self.repeats)), digit = self.latex(str(self.digit)))

	def question_answer(self):
		return transform(self.number, self.base ** self.degree, self.digits)
