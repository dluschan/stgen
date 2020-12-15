from .common import Task09
from random import sample, randint


class Type0(Task09):
	"""Кодирование звуковой информации"""
	def __init__(self):
		super().__init__()
		self.audio_file = ''
		self.question = """Производилась {channels} звукозапись с частотой дискретизации {freq}
		и {bits} разрешением. В результате был получен файл размером {size}. Сжатие данных не производилось.
		Определите сколько времени проводилась запись.
		Ответ выразите в минутах и округлите до целого."""

	def category(self):
		return super().category() + 'Тип 0/'

	def question_text(self):
		return self.question.format(
			channels="двухканальная (стерео)",
			freq="64 кГц",
			bits="24-битным",
			size="48 Мбайт"
		)

	def question_answer(self):
		return self.ans


class SubtypeA(Type0):
	"""Восстановление кода по 4 известным буквам."""
	def __init__(self):
		self.absent = 1
		super().__init__()

	def category(self):
		return super().category() + 'Подтип A'


