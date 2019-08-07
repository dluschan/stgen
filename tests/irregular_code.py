import unittest
from stgen.tools.irregular_code import code


class MyTestCase(unittest.TestCase):
	def test_0(self):
		letters = ('A', 'B', 'C')
		frequency = (10, 2, 2)
		x = code(letters, frequency)
		self.assertEqual(len(x['A']), 1)
		self.assertEqual(len(x['B']), 2)
		self.assertEqual(len(x['C']), 2)

	def test_1(self):
		letters = ('A', 'B', 'C', 'D')
		frequency = (1, 1, 1, 1)
		x = code(letters, frequency)
		self.assertEqual(len(x['A']), 2)
		self.assertEqual(len(x['B']), 2)
		self.assertEqual(len(x['C']), 2)
		self.assertEqual(len(x['D']), 2)

	def test_2(self):
		letters = ('A', 'B', 'C', 'D')
		x = code(letters)
		self.assertEqual(len(x['A']), 2)
		self.assertEqual(len(x['B']), 2)
		self.assertEqual(len(x['C']), 2)
		self.assertEqual(len(x['D']), 2)

	def test_3(self):
		letters = ('A', 'B', 'C',)
		x = code(letters)
		self.assertEqual(len(x['A']) + len(x['B']) + len(x['C']), 5)

	def test_4(self):
		letters = ('A', 'B', 'C', 'D')
		frequency = (10, 5, 1, 1)
		x = code(letters, frequency)
		self.assertEqual(len(x['A']), 1)
		self.assertEqual(len(x['B']), 2)
		self.assertEqual(len(x['C']), 3)
		self.assertEqual(len(x['D']), 3)


if __name__ == '__main__':
	unittest.main()
