from ..tools.task import BaseTask
from random import choice, sample, randint


class Task05(BaseTask):
	"""ЕГЭ по информатике - Задача номер 5"""
	def __init__(self):
		self.count = randint(3, 7)
		self.notations = {2: 'двоичной', 3: 'троичной', 4: 'четверичной', 5: 'пятеричной', 6: 'шестеричной', 7: 'семеричной', 8: 'восьмеричной', 9: 'девятеричной', 10: 'десятичной', 11: 'одиннадцатеричной', 12: 'двенадцатеричной', 13: 'тринадцатеричной', 14: 'четырнадцатеричной', 15: 'пятнадцатеричной', 16: 'шестнадцатеричной', 17: 'семнадцатеричной', 18: 'восемнадцатеричной', 19: 'девятнадцатеричной', 20: 'двадцатеричной'}
		latin_big = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		latin_small = "abcdefghijklmnopqrstuvwxyz"
		cyrillic_big = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
		cyrillic_small = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
		greek_big = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
		greek_small = "αβγδεζηθικλμνξοπρστυφχψω"
		self.letters = ''.join(sorted(sample(
			choice([latin_big, latin_small, cyrillic_big, cyrillic_small, greek_big, greek_small]),
			self.count
		)))

	def notation(self, base):
		assert 1 < base < 37, base
		return 'в ' + self.notations[base] + ' системе счисления' if base in self.notations else 'в системе счисления с основанием ' + self.latex(base)

