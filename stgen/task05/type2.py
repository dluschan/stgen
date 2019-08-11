from ..tools.notation import transform
from .common import Task05
from random import sample, randint


class Type2(Task05):
	"""Равномерный пятисимвольный бинарный код с разницей между любой парой кодов не менее чем в трёх позициях.

	Кодирование осуществляется по следующей схеме:
	A --00111--> B --11100--> C --00111--> D --11100--> A,
	где A - произвольное кодовое слово, а единица в операторе стрелка инвертирует соответствующий разряд.
	Благодаря этому достигаются следующие инварианты:
	пары A<->C и B<->D отличаются ровно в 4 разрядах, остальные - в трёх.
	Техническая реализация:
	B = A ^ 7  # 00111 == 7
	C = A ^ 27 # 11011 == 27
	D = A ^ 28 # 11100 == 28"""
	def __init__(self):
		super().__init__()
		self.count = 4
		self.sym = '\\#'
		self.letters = sample(self.alphabetic, self.count)
		a = randint(0, 2**5 - 1)
		self.table = dict(zip(self.letters, map(lambda x: transform(x, 2, width=5), (a, a ^ 7, a ^ 27, a ^ 28))))
		self.rest, self.ans = self.table.popitem()
		self.masked = list(self.ans)
		for i in sample(range(5), self.absent):
			self.masked[i] = self.sym
		self.table[self.rest] = ''.join(self.masked)
		self.question = """Для кодирования некоторой последовательности, состоящей из букв {letters},
		решили использовать равномерный двоичный код длиной 5 символов, для которого каждая пара кодовых слов
		отличается по меньшей мере в трёх позициях. {definite} Символом {sym} обозначены неизвестыне биты.
		Восстановите полное кодовое слово для буквы {rest}."""

	def category(self):
		return super().category() + 'Тип 2/'

	def question_text(self):
		return self.question.format(
			letters=', '.join(self.letters),
			definite=self.definite(),
			rest=self.rest,
			sym=self.sym
		)

	def question_answer(self):
		return self.ans


class SubtypeA(Type2):
	"""Восстановление кода по 4 известным буквам."""
	def __init__(self):
		self.absent = 1
		super().__init__()

	def category(self):
		return super().category() + 'Подтип A'


class SubtypeB(Type2):
	"""Восстановление кода по 3 известным буквам."""
	def __init__(self):
		self.absent = 2
		super().__init__()

	def category(self):
		return super().category() + 'Подтип B'


class SubtypeC(Type2):
	"""Восстановление кода по 2 известным буквам."""
	def __init__(self):
		self.absent = 3
		super().__init__()

	def category(self):
		return super().category() + 'Подтип C'


class SubtypeD(Type2):
	"""Восстановление кода по 1 известным буквам."""
	def __init__(self):
		self.absent = 4
		super().__init__()

	def category(self):
		return super().category() + 'Подтип D'


class SubtypeE(Type2):
	"""Восстановление кода без известным букв."""
	def __init__(self):
		self.absent = 5
		super().__init__()

	def category(self):
		return super().category() + 'Подтип E'

