from random import choices
from .common import *


class Type3(Task16):
	"""Слова одинаковой длины в словарном порядке."""
	def __init__(self):
		super().__init__()
		self.question = """Все {width}-буквенные слова, составленные из букв {letters}, записаны в алфавитном порядке.
		Вот начало списка:<br>
		{list}
		{question}
		"""
		self.width = randint(3, 5)
		self.count = randint(2, 6)
		latin_big = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		latin_small = 'abcdefghijklmnopqrstuvwxyz'
		cyrillic_big = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
		cyrillic_small = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
		self.letters = ''.join(sorted(sample(
			choice([latin_big, latin_small, cyrillic_big, cyrillic_small]),
			self.count
		)))
		self.dict = str.maketrans(self.letters, self.digits[:self.count])
		self.list = ''.join(str(i+1) + '. ' + transform(i, self.count, self.letters).rjust(self.width, self.letters[0]) + '<br>' + '\n' for i in range(self.count + 1))

	def category(self):
		return super().category() + 'Тип 3/'

	def question_text(self):
		return self.question.format(
			width=self.latex(self.width),
			letters=self.latex(', '.join(self.letters)),
			list=self.list,
			question=self.subtype_question
		)


class SubtypeA(Type3):
	"""Определение слова по его номеру."""
	def __init__(self):
		super().__init__()
		self.row = randint(self.count**(self.width - 1), self.count**self.width)
		self.subtype_question = "Определите слово, которое стоит под номером {row}.".format(row=self.row)

	def category(self):
		return super().category() + 'Подтип A'

	def question_answer(self):
		return transform(self.row - 1, self.count, self.letters)


class SubtypeB(Type3):
	"""Определение номера первого слова, начинающегося с определённых букв."""
	def __init__(self):
		super().__init__()
		self.determinate = randint(1, self.width - 1)
		self.prefix = choice(self.letters[1:]) + ''.join(choices(self.letters, k=self.determinate - 1))
		self.subtype_question = "Определите номер первого слова, которое начинается с {let} {prefix}.".format(
			let='буквы' if self.determinate == 1 else 'букв',
			prefix=self.prefix
		)

	def category(self):
		return super().category() + 'Подтип B'

	def question_answer(self):
		return int((self.prefix + self.letters[0] * (self.width - self.determinate)).translate(self.dict), self.count) + 1


class SubtypeC(Type3):
	"""Определение номера слова."""

	def __init__(self):
		super().__init__()
		self.word = choice(self.letters[1:]) + ''.join(choices(self.letters, k=self.width - 1))
		self.subtype_question = "Определите номер слова {word}.".format(word=self.word)

	def category(self):
		return super().category() + 'Подтип С'

	def question_answer(self):
		return int(self.word.translate(self.dict), self.count) + 1

