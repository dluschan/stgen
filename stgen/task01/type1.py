from .common import *
from collections import Counter


class Type1(Task1):
	"""Определение показателей, связанных с цифрами чисел в разных системах счисления."""
	def __init__(self):
		super().__init__()
		self.base, self.degree = self.linked()

	def category(self):
		return super().category() + "Тип 1/"

	def question_text(self):
		return self.question.format(number=self.based(self.number, choice([self.base ** self.degree] * 9 + [10])), notation=self.notation(self.base))


class SubtypeA(Type1):
	"""Количество повторений некоторой цифры числа в разных системах счисления."""
	def __init__(self):
		super().__init__()
		self.question = "Определите сколько цифр {digit} содержит число {number} в {notation}."
		self.digit = choice(self.digits[:self.base])

	def category(self):
		return super().category() + "Подтип A"

	def question_text(self):
		return self.question.format(digit=self.digit, number=self.based(self.number, choice([self.base ** self.degree] * 9 + [10])), notation=self.notation(self.base))

	def question_answer(self):
		return transform(self.number, self.base, self.digits).count(self.digit)


class SubtypeB(Type1):
	"""Количество значащих цифр числа в разных системах счисления."""
	def __init__(self):
		super().__init__()
		self.question = "Определите сколько значащих цифр содержит число {number} в {notation}."

	def category(self):
		return super().category() + "Подтип B"

	def question_answer(self):
		return len(transform(self.number, self.base, self.digits))


class SubtypeC(Type1):
	"""Количество различных цифр числа в разных системах счисления."""
	def __init__(self):
		super().__init__()
		self.question = "Определите сколько различных цифр содержит число {number} в {notation}."

	def category(self):
		return super().category() + "Подтип B"

	def question_answer(self):
		return len(set(transform(self.number, self.base, self.digits)))


class SubtypeD(Type1):
	"""Самая большая цифра числа в разных системах счисления."""
	def __init__(self):
		super().__init__()
		self.question = "Определите самую большую цифру числа {number} в {notation}."

	def category(self):
		return super().category() + "Подтип D"

	def question_answer(self):
		return max(transform(self.number, self.base, self.digits))


class SubtypeE(Type1):
	"""Самая маленькая цифра числа в разных системах счисления."""
	def __init__(self):
		super().__init__()
		self.question = "Определите самую маленькую цифру числа {number} в {notation}."

	def category(self):
		return super().category() + "Подтип E"

	def question_answer(self):
		return min(transform(self.number, self.base, self.digits))


class SubtypeF(Type1):
	"""Наибольшая из самых часто встречающихся цифр числа в разных системах счисления."""
	def __init__(self):
		super().__init__()
		self.question = "Определите самую часто встречающуюся цифру числа {number} в {notation}. Если чаще других встречаются несколькьо цифр, укажите наибольшую из них."

	def category(self):
		return super().category() + "Подтип F"

	def question_answer(self):
		return max([(element[1], element[0]) for element in Counter(transform(self.number, self.base, self.digits)).items()])[1]


class SubtypeG(Type1):
	"""Наименьшая из самых часто встречающихся цифр числа в разных системах счисления."""
	def __init__(self):
		super().__init__()
		self.question = "Определите самую часто встречающуюся цифру числа {number} в {notation}. Если чаще других встречаются несколькьо цифр, укажите наименьшую из них."

	def category(self):
		return super().category() + "Подтип G"

	def question_answer(self):
		return min([(-element[1], element[0]) for element in Counter(transform(self.number, self.base, self.digits)).items()])[1]


class SubtypeH(Type1):
	"""Наибольшая из самых редко встречающихся цифр числа в разных системах счисления."""
	def __init__(self):
		super().__init__()
		self.question = "Определите самую редко встречающуюся цифру числа {number} в {notation}. Если реже других встречаются несколькьо цифр, укажите наибольшую из них."

	def category(self):
		return super().category() + "Подтип H"

	def question_answer(self):
		return max([(-element[1], element[0]) for element in Counter(transform(self.number, self.base, self.digits)).items()])[1]


class SubtypeI(Type1):
	"""Наименьшая из самых редко встречающихся цифр числа в разных системах счисления."""
	def __init__(self):
		super().__init__()
		self.question = "Определите самую редко встречающуюся цифру числа {number} в {notation}. Если реже других встречаются несколькьо цифр, укажите наименьшую из них."

	def category(self):
		return super().category() + "Подтип I"

	def question_answer(self):
		return min([(element[1], element[0]) for element in Counter(transform(self.number, self.base, self.digits)).items()])[1]

