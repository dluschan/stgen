from ..tools.notation import transform
from ..tools.choices import choices
from ..tools.irregular_code import code, codebook
from collections import Counter
from random import sample, choice, shuffle
from .common import *


class Type1(Task05):
	"""Восстановление отсутствующих кодовых слов."""
	def __init__(self):
		super().__init__()

	def category(self):
		return super().category() + 'Тип 1/'


class SubtypeA(Type1):
	"""Восстановление кода одной буквы."""
	def __init__(self):
		super().__init__()
		self.extreme = choice([(min, 'наименьшим'), (max, 'наибольшим')])
		self.frequency = sample(range(100), len(self.letters))
		self.table = code(self.letters, self.frequency)
		self.rest, code_a = self.table.popitem()
		absent, code_b = self.table.popitem()
		self.letters = list(self.letters)
		self.letters.remove(absent)
		if len(code_a) == len(code_b) and code_a[:-1] == code_b[:-1]:
			self.ans = code_a[:-1]
		elif len(code_a) == len(code_b):
			self.ans = self.extreme[0](code_a, code_b)
		else:
			self.ans = min(code_a, code_b, key=len)
		self.question = """Для кодирования некоторой последовательности, состоящей из букв {letters}, 
		решили использовать неравномерный двоичный код, удовлетворяющий условию Фано.
		{definite} Укажите кратчайшее кодовое слово для буквы {rest}.
		Если таких кодовых слов несколько, укажите код с {extreme} числовым значением."""

	def category(self):
		return super().category() + 'Подтип A'

	def question_text(self):
		return self.question.format(
			letters=', '.join(self.letters),
			definite=self.definite(),
			rest=self.rest,
			extreme=self.extreme[1]
		)

	def question_answer(self):
		return self.ans


class SubtypeB(Type1):
	"""Восстановление кода одной из двух неизвестных букв."""
	def __init__(self):
		super().__init__()
		self.extreme = choice([(min, 'наименьшим'), (max, 'наибольшим')])
		self.frequency = sample(range(100), len(self.letters))
		self.table = code(self.letters, self.frequency)
		self.rest, code_a = self.table.popitem()
		absent, code_b = self.table.popitem()
		self.letters = list(self.letters)
		if len(code_a) == len(code_b):
			self.ans = self.extreme[0](code_a, code_b)
		else:
			self.ans = min(code_a, code_b, key=len)
		self.question = """Для кодирования некоторой последовательности, состоящей из букв {letters}, 
		решили использовать неравномерный двоичный код, удовлетворяющий условию Фано.
		{definite} Укажите кратчайшее кодовое слово для буквы {rest}.
		Если таких кодовых слов несколько, укажите код с {extreme} числовым значением."""

	def category(self):
		return super().category() + 'Подтип B'

	def question_text(self):
		return self.question.format(
			letters=', '.join(self.letters),
			definite=self.definite(),
			rest=self.rest,
			extreme=self.extreme[1]
		)

	def question_answer(self):
		return self.ans


class SubtypeC(Type1):
	"""Восстановление кода нескольких букв для оптимального кодирования заданного слова."""
	def __init__(self):
		super().__init__()
		self.table = code(self.letters)
		self.ans = sum(map(len, self.table.values()))
		self.hidden = randint(self.count // 2 - 1, self.count // 2 + 1)
		for _ in range(self.hidden):
			self.table.popitem()
		self.letters = list(self.letters)
		self.question = """Для кодирования некоторой последовательности, состоящей из букв {letters}, 
		решили использовать неравномерный двоичный код, удовлетворяющий условию Фано.
		{definite} Укажите какая наименьшая возможная суммарная длина всех кодовых слов."""

	def category(self):
		return super().category() + 'Подтип C'

	def question_text(self):
		return self.question.format(
			letters=', '.join(self.letters),
			definite=self.definite()
		)

	def question_answer(self):
		return self.ans


class SubtypeD(Type1):
	"""Восстановление кода нескольких букв."""
	def __init__(self):
		super().__init__()
		self.frequency = choices(range(1, 6), k=len(self.letters))
		self.absent = randint(self.count // 3 - 1, self.count // 3 + 1)
		self.frequency = self.frequency[:-self.absent] + [0] * self.absent
		self.table = code(self.letters, self.frequency)
		r = []
		for a, k in zip(self.letters, self.frequency):
			r += [a] * k
		shuffle(r)
		self.word = ''.join(r)
		self.ans = sum(map(lambda x: len(self.table[x]) * self.frequency[self.letters.index(x)], self.letters))
		self.hidden = randint(self.count // 2 - 1, self.count // 2 + 1)
		for _ in range(self.hidden):
			self.table.popitem()
		self.letters = list(self.letters)
		self.question = """Для кодирования некоторой последовательности, состоящей из букв {letters}, 
		решили использовать неравномерный двоичный код, удовлетворяющий условию Фано.
		{definite} Укажите какое наименьшее количество двоичных знаков потребуется для кодирования слова {word}."""

	def category(self):
		return super().category() + 'Подтип D'

	def question_text(self):
		return self.question.format(
			letters=', '.join(self.letters),
			definite=self.definite(),
			word=self.word
		)

	def question_answer(self):
		return self.ans

