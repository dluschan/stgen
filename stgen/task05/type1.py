from ..tools.notation import transform
from ..tools.choices import choices
from .common import *
from math import log


class Type1(Task05):
	"""Поиск системы счисления числа."""
	def __init__(self):
		super().__init__()
		self.word = ''.join(choices(self.letters, k=randint(2, 8)))
		self.question = """Для кодирования некоторой последовательности, состоящей из букв {letters}, 
		решили использовать неравномерный двоичный код, удовлетворяющий условию Фано.
		{definited} Какова наименьшая возможная сумма длин кодовых слов для букв {rest}?"""
		self.code = int(''.join((transform(self.letters.index(letter), self.base, width=self.width) for letter in self.word)), self.base)

	def category(self):
		return super().category() + 'Тип 1'

	def question_text(self):
		return self.question.format(
			letters=self.latex(', '.join(self.letters)),
			numbers=self.latex(', '.join(map(str, range(self.count)))),
			base=self.notation(self.base),
			width=self.width,
			word=self.word,
			notation=self.notation(self.base ** self.degree)
		)

	def question_answer(self):
		return transform(self.code, self.base ** self.degree)

