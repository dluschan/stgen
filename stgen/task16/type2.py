from .common import *


class Type2(Task16):
	"""Поиск чисел, оканчивающихся на заданный суффикс в некоторой системе счисления."""
	def __init__(self):
		super().__init__()
		self.question = """Найдите все натуральные числа, не превосходящие {limit}, 
		запись которых {base} оканчивается на {suffix}.
		{question}"""
		self.width = randint(1, 4 if self.base < 10 else 3)
		self.suffix = randint(1, self.base ** self.width - 1)
		self.count = self.degree - int(log(self.base ** self.width, 10))
		self.limit = randint(self.base ** self.width + self.suffix, self.base ** self.width * self.count + self.suffix - 1)
		self.top = (self.limit - self.suffix) // self.base ** self.width

	def category(self):
		return super().category() + 'Тип 2/'

	def question_text(self):
		return self.question.format(
			limit=self.latex(self.limit),
			base=self.notation(self.base),
			suffix=transform(self.suffix, self.base, width=self.width),
			question=self.subtype_question
		)


class SubtypeA(Type2):
	"""Явный поиск чисел, оканчивающихся на заданный суффикс в некоторой системе счисления."""
	def __init__(self):
		self.degree = 9
		self.subtype_question = "В ответ запишите все найденные числа в порядке возрастания друг за другом без разделителей."
		super().__init__()

	def category(self):
		return super().category() + 'Подтип A/'

	def question_answer(self):
		return ''.join(map(str, [self.suffix + self.base ** self.width * k for k in range(self.top + 1)]))


class SubtypeB(Type2):
	"""Поиск количества чисел, оканчивающихся на заданный суффикс в некоторой системе счисления."""
	def __init__(self):
		self.degree = 109
		self.subtype_question = "В ответ запишите количество найденных чисел."
		super().__init__()

	def category(self):
		return super().category() + 'Подтип B/'

	def question_answer(self):
		return self.top + 1

