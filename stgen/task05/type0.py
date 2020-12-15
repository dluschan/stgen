from ..tools.notation import transform
from .common import Task05
from math import log
from random import choices, randint


class Type0(Task05):
	"""Кодирование букв в разных системах счисления."""
	def __init__(self):
		super().__init__()
		self.base = randint(2, 6)
		self.degree = randint(1, int(log(36, self.base)))
		self.width = randint(2, 4)
		self.word = ''.join(choices(self.letters, k=randint(2, 8)))
		self.question = """Для кодирования букв {letters} решили использовать кодовые слова, 
		представляющие собой числа {numbers} {base} соответственно и имеющие не меньше {width} букв. 
		Закодируйте слово {word} таким способом и результат запишите {notation}."""
		self.code = int(''.join((transform(self.letters.index(letter), self.base, width=self.width) for letter in self.word)), self.base)

	def category(self):
		return super().category() + 'Тип 0'

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

