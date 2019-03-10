from .common import *


class Type0(Task15):
	def __init__(self):
		super().__init__()

	def category(self):
		return super().category() + 'Тип 0'

