import unittest
from use.tools.decompose import *

class TestDecompose(unittest.TestCase):
	def test_empty(self):
		self.assertEqual(positive(150, 2, 10), set())

	def test_empty2(self):
		self.assertEqual(positive(20, 2, 10), set())

	def test_zero(self):
		self.assertEqual(positive(0, 2, 1), {1})

	def test_zero2(self):
		self.assertEqual(positive(0, 2, 100), {1})

	def test_empty_neg(self):
		self.assertEqual(positive(-1, 2, 1), {})

	def test_neg(self):
		self.assertEqual(positive(-1, 2, 2), {1})

	def test_neg2(self):
		self.assertEqual(positive(-1, 2, 100), {1})

	def test_one(self):
		self.assertEqual(positive(19, 3, 10), {2})

	def test_two(self):
		self.assertEqual(positive(5, 2, 10), {1})

	def test_three(self):
		self.assertEqual(positive(5, 10, 10), {2, 3, 4, 5, 6, 7, 8, 9})

	def test_minimum_count_pos_terms(self):
		self.assertEqual(minimum_count_pos_terms([10, 20, 30], 5), 8)

	def test_minimum_count_pos_terms2(self):
		self.assertEqual(minimum_count_pos_terms([10, 2, 17], 5), 5)

	def test_minimum_count_pos_terms3(self):
		self.assertEqual(minimum_count_pos_terms([10, 2, 17], 50), 2)

	def test_positive_edge(self):
		self.assertEqual(positive_edge(20, 3, 1, 10), (21, 30))

	def test_single_decompose(self):
		for _ in range(100):
			k = randint(2, 100)
			limit = randint(1, 35)
			x = randint(k, k*limit)
			res = single_decompose(x, k, limit)
			self.assertEqual(sum(res), x)
			self.assertEqual(len(res), k)
			self.assertTrue(all([y > 0 for y in res]))

	def test_binary_decompose(self):
		for _ in range(100):
			k_pos = randint(1, 10)
			k_neg = randint(1, 10)
			limit = randint(1, 35)
			x = randint(k_pos-limit*k_neg, limit*k_pos-k_neg)
			res = binary_decompose(x, k_pos, k_neg, limit)
			self.assertEqual(sum(res[0]) - sum(res[1]), x)
			self.assertEqual(len(res[0]), k_pos)
			self.assertEqual(len(res[1]), k_neg)
			self.assertTrue(all([y > 0 for y in res[0]]))
			self.assertTrue(all([y > 0 for y in res[1]]))

	def test_decompose(self):
		for _ in range(100):
			limit = randint(1, 35)
			x = randint(1, 1000)
			res = decompose([x], limit)
			self.assertEqual(len(res), 1)
			self.assertEqual(sum(res[0][0]) - sum(res[0][1]), x)
			self.assertTrue(all([y > 0 for y in res[0][0]]))
			self.assertTrue(all([y > 0 for y in res[0][1]]))
