from .common import *


class Type0(Task22):
	def __init__(self):
		super().__init__()

	def category(self):
		return super().category() + 'Тип 0/'


class SubtypeA(Type0):
	"""Количество вариантов равно 0."""
	def __init__(self):
		self.edge = [0, 0]
		super().__init__()

	def category(self):
		return super().category() + 'Подтип A'


class SubtypeB(Type0):
	"""Количество вариантов от 1 до 99 включительно."""
	def __init__(self):
		self.edge = [1, 99]
		super().__init__()

	def category(self):
		return super().category() + 'Подтип B'


class SubtypeC(Type0):
	"""Количество вариантов от 99 до 499 включительно."""
	def __init__(self):
		self.edge = [99, 499]
		super().__init__()

	def category(self):
		return super().category() + 'Подтип C'


class SubtypeD(Type0):
	"""Количество вариантов от 500 до 999 включительно."""
	def __init__(self):
		self.edge = [500, 999]
		super().__init__()

	def category(self):
		return super().category() + 'Подтип D'


