from .common import *


class Type0(Task01):
	"""Превод чисел в разные системы счисления."""
	def __init__(self):
		super().__init__()
		self.question = "Представьте число {number} в {notation}."

	def category(self):
		return super().category() + "Тип 0/"


class SubtypeA(Type0):
	"""Превод чисел из десятичной в произвольные системы счисления."""
	def __init__(self):
		super().__init__()

	def category(self):
		return super().category() + "Подтип A"

	def question_text(self):
		return self.question.format(number=self.latex(self.number), notation=self.notation(self.base))

	def question_answer(self):
		return transform(self.number, self.base, self.digits)


class SubtypeB(Type0):
	"""Превод чисел из произвольных систем счисления в десятичную."""
	def __init__(self):
		super().__init__()

	def category(self):
		return super().category() + "Подтип B"

	def question_text(self):
		return self.question.format(number=self.based(self.number, self.base), notation=self.notation(10))

	def question_answer(self):
		return self.number


class SubtypeC(Type0):
	"""Превод чисел в разных системах счисления по разрядам в систему счисления с большим основанием."""
	def __init__(self):
		super().__init__()
		self.base, self.degree=self.linked()

	def category(self):
		return super().category() + "Подтип C"

	def question_text(self):
		return self.question.format(number=self.based(self.number, self.base), notation=self.notation(self.base ** self.degree))

	def question_answer(self):
		return transform(self.number, self.base ** self.degree, self.digits)


class SubtypeD(Type0):
	"""Превод чисел в разных системах счисления по разрядам в систему счисления с меньшим основанием."""
	def __init__(self):
		super().__init__()
		self.base, self.degree=self.linked()

	def category(self):
		return super().category() + "Подтип D"

	def question_text(self):
		return self.question.format(number=self.based(self.number, self.base ** self.degree), notation=self.notation(self.base))

	def question_answer(self):
		return transform(self.number, self.base, self.digits)


class SubtypeE(Type0):
	"""Превод чисел в разных системах счисления по разрядам с помощью промежуточной системы счисления."""
	def __init__(self):
		super().__init__()
		self.source_base, self.target_base=sorted(choice([[4, 8], [4, 32], [8, 16], [8, 32], [16, 32], [9, 27]]), reverse=choice([True, False]))

	def category(self):
		return super().category() + "Подтип E"

	def question_text(self):
		return self.question.format(number=self.based(self.number, self.source_base), notation=self.notation(self.target_base))

	def question_answer(self):
		return transform(self.number, self.target_base, self.digits)

