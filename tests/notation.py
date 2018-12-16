import unittest
from stgen.tools.notation import *


class TestTransform(unittest.TestCase):
	"""Тестирование перевода чисел в разные системы счисления."""
	def test_transform(self):
		self.assertEqual(transform(255, 2), '11111111')

	def test_transform_zero(self):
		self.assertEqual(transform(0, 5), '0')

	def test_transform_abc(self):
		self.assertEqual(transform(255, 2, 'qw'), 'wwwwwwww')

	def test_transform_based(self):
		self.assertEqual(transform(255, 2, based = True), '11111111_{2}')

	def test_transform_error(self):
		self.assertRaises(IndexError, transform, 255, 2, 'q')


class TestLimitedNumber(unittest.TestCase):
	"""Тестирование подбора чисел по цифрам в разных системах счисления."""
	def test_min_1(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 2, 2, 2, 1), '1000')

	def test_min_2(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 2, 2, 2, 2), '1010')

	def test_min_3(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 6, 4, 7, 2), '1000000001110111')

	def test_min_4(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 2, 1, 1, 1), '1000')

	def test_min_5(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 2, 1, 1, 2), '1001')

	def test_min_6(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 2, 1, 1, 3), '1011')

	def test_min_7(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 2, 1, 1, 4), '1111')

	def test_min_8(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 2, 1, 1, 5), '11111')

	def test_min_9(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 2, 1, 1, 6), '111111')

	def test_min_10(self):
		self.assertRaises(AssertionError, minLimitedNumberStr, 2, 3, 2, 1, 1, 7)

	def test_min_11(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 2, 1, 0, 2), '1001')

	def test_min_12(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 2, 1, 0, 3), '1000')

	def test_min_13(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 2, 1, 0, 4), '10000')

	def test_min_14(self):
		self.assertEqual(minLimitedNumberStr(2, 3, 3, 4, 0, 1), '1000000')

	def test_max_1(self):
		self.assertEqual(maxLimitedNumberStr(2, 2, 3, 4, 3, 1), '111111')

	def test_max_2(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 3, 3, 7, 1), '111110110110')

	def test_max_2_5(self):
		self.assertEqual(maxLimitedNumberStr(2, 5, 2, 3, 7, 1), '1111110110')

	def test_max_3(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 3, 3, 7, 2), '111111110110')

	def test_max_4(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 3, 3, 7, 3), '111111111110')

	def test_max_5(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 3, 3, 7, 4), '111111111111')

	def test_max_6(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 3, 3, 5, 1), '111111111101')

	def test_max_7(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 3, 3, 5, 2), '111111101101')

	def test_max_8(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 3, 3, 5, 3), '111101101101')

	def test_max_9(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 3, 3, 5, 4), '101101101101')

	def test_max_10(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 2, 3, 3, 1), '11111111')

	def test_max_11(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 2, 3, 3, 2), '11111011')

	def test_max_12(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 2, 3, 3, 3), '011011011')

	def test_max_13(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 2, 3, 4, 1), '11111100')

	def test_max_14(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 2, 3, 4, 2), '11100100')

	def test_max_15(self):
		self.assertRaises(AssertionError, maxLimitedNumberStr, 2, 4, 2, 3, 4, 3)

	def test_max_16(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 2, 3, 1, 1), '11111001')

	def test_max_17(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 2, 3, 1, 2), '11001001')

	def test_max_18(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 2, 3, 1, 3), '001001001')

	def test_max_19(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 2, 3, 0, 1), '11111000')

	def test_max_20(self):
		self.assertEqual(maxLimitedNumberStr(2, 4, 2, 3, 0, 2), '11000000')

	def test_max_21(self):
		self.assertRaises(AssertionError, maxLimitedNumberStr, 2, 4, 2, 3, 0, 3)

