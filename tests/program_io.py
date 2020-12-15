import unittest
from stgen.tools.program_io import *


class TestIOFormat(unittest.TestCase):
	"""Тестирование генерации описания входных и выходных данных для задач на программирование."""
	def test_input_0(self):
		params = {'n': [int, [1, 10 ** 4], 'количество чисел']}
		input_format = """n"""
		self.assertEqual(parse_input(input_format, params), """<br>Формат входных данных<br>В единственной строке задаётся количество чисел \\( n \\).""")

	def test_output_0(self):
		params = {'s': [int, None, 'искомая сумма']}
		output_format = """s"""
		self.assertEqual(parse_output(output_format, params), """<br>Формат выходных данных<br>В единственной строке выводится искомая сумма \\( s \\).""")

	def test_input_1(self):
		params = {
			'n': [int, [1, 10 ** 4], 'количество чисел'],
			'x': [int, [1, 2 ** 30], 'чисел']
		}
		input_format = """n
x*n"""
		self.assertEqual(parse_input(input_format, params), """<br>Формат входных данных<br>В первой строке задаётся количество чисел \\( n \\). В следующей строке задаётся \\( n \\) чисел \\( x \\).""")

	def test_output_1(self):
		params = {
			'k': [int, [1, 10 ** 4], 'количество пар чисел'],
			's': [int, [1, 10 ** 4], 'высоты']
		}
		output_format = """s|k"""
		self.assertEqual(parse_output(output_format, params), """<br>Формат выходных данных<br>В \\( k \\) строках выводятся высоты \\( s \\).""")


class TestInputGenerate(unittest.TestCase):
	"""Тестирование генерации входных данных для задач на программирование."""
	def test_0(self):
		params = {'n': [int, [1, 10 ** 4], 'количество чисел']}
		input_format = """n"""
		s = generate_input(input_format, params)
		self.assertTrue(params[input_format][1][0] <= params[input_format][0](s) <= params[input_format][1][1])

	def test_1(self):
		params = {
			'n': [int, [1, 10], 'количество чисел'],
			'x': [float, [1, 10**3], 'число'],
		}
		input_format = """n
x|n"""
		s = generate_input(input_format, params)
		head, *tail, empty = s.split("\n")
		self.assertEqual(params["n"][0](head), len(tail))
		for num in tail:
			self.assertTrue(params["x"][1][0] <= params["x"][0](num) <= params["x"][1][1])

	def test_2(self):
		params = {
			'n': [int, [1, 10], 'количество чисел'],
			'x': [float, [1, 10**3], 'число'],
		}
		input_format = """n
x*n"""
		s = generate_input(input_format, params)
		head, tail, empty = s.split("\n")
		tail = tail.split()
		self.assertEqual(params["n"][0](head), len(tail))
		for num in tail:
			self.assertTrue(params["x"][1][0] <= params["x"][0](num) <= params["x"][1][1])

