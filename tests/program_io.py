import unittest
from stgen.tools.program_io import *


class TestIOFormat(unittest.TestCase):
	"""Тестирование генерации входных и выходных данных для задач на программирование."""
	def test_input_0(self):
		params = {'n': [int, [1, 10 ** 4], 'количество чисел']}
		input_format = """n"""
		self.assertEqual(parse_input(input_format, params), """Формат входных данных
В единственной строке задаётся количество чисел \\( n \\).""")

	def test_output_0(self):
		params = {'s': [int, None, 'искомая сумма']}
		output_format = """s"""
		self.assertEqual(parse_output(output_format, params), """Формат выходных данных
В единственной строке выводится искомая сумма \\( s \\).""")

	def test_input_1(self):
		params = {
			'n': [int, [1, 10 ** 4], 'количество чисел'],
			'x': [int, [1, 2 ** 30], 'чисел']
		}
		input_format = """n
x*n"""
		self.assertEqual(parse_input(input_format, params), """Формат входных данных
В первой строке задаётся количество чисел \\( n \\). В следующей строке задаётся \\( n \\) чисел \\( x \\).""")

	def test_output_1(self):
		params = {
			'k': [int, [1, 10 ** 4], 'количество пар чисел'],
			's': [int, [1, 10 ** 4], 'высоты']
		}
		output_format = """s|k"""
		self.assertEqual(parse_output(output_format, params), """Формат выходных данных
В \\( k \\) строках выводятся высоты \\( s \\).""")
