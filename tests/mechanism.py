import unittest
from use.task22.common import *


class MechanismCommandTest(unittest.TestCase):
	def test_eq(self):
		a = Addition(1)
		b = Addition(1)
		self.assertEqual(a, b)


class MechanismTest(unittest.TestCase):
	def test_0(self):
		m = Mechanism([Addition(1), Multiplication(2), Multiplication(3)], [3, 15, 50], [33])
		self.assertEqual(m(), 121)

	def test_1(self):
		m = Mechanism([Addition(1), Addition(8)], [1, 52], [27])
		self.assertEqual(m(), 10590)

	def test_2(self):
		m = Mechanism([Addition(1), Addition(6), Multiplication(4)], [10, 52], [])
		self.assertEqual(m(), 17902)

	def test_3(self):
		m = Mechanism([Addition(3), Addition(7), Addition(9)], [8, 43, 56], [31, 35])
		self.assertEqual(m(), 399)

	def test_4(self):
		m = Mechanism([Addition(3), Addition(8)], [5, 56], [37])
		self.assertEqual(m(), 198)

	def test_5(self):
		m = Mechanism([Addition(1), Addition(3)], [5, 96], [])
		self.assertEqual(m(), 781666575692345)

	def test_6(self):
		m = Mechanism([Addition(1), Multiplication(2)], [6, 48, 49, 83], [13])
		self.assertEqual(m(), 44)

	def test_7(self):
		m = Mechanism([Addition(1), Multiplication(2), Multiplication(3), Duplication()], [8, 100], [31])
		self.assertEqual(m(), 585)

	def test_8(self):
		m = Mechanism([Addition(4), Addition(5)], [8, 58, 63, 73, 90], [16, 26, 35, 42, 48])
		self.assertEqual(m(), 484)
