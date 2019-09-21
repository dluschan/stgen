import unittest
from stgen.tools.unit import *


class UnitTest(unittest.TestCase):
	def test_time_compare(self):
		s0 = Second(1)
		s1 = Second(120)
		s2 = Second(108000)
		m0 = Minute(0.1)
		m1 = Minute(2)
		m2 = Minute(150)
		h0 = Hour(1)
		h1 = Hour(2.5)
		h2 = Hour(30)
		self.assertEqual(1, 1.0)
		self.assertEqual(s2, h2)
		self.assertEqual(m2, h1)
		self.assertLess(s0, s1)
		self.assertLess(s0, m0)
		self.assertLess(s0, m1)
		self.assertGreater(h0, s1)
		self.assertGreater(h0, m1)
		self.assertListEqual(sorted([s0, s1, s2, m0, m1, m2, h0, h1, h2]), [s0, m0, s1, m1, h0, m2, h1, s2, h2])

	def test_prefix_info_compare(self):
		x = kibi(Bit(1))
		y = Bit(1000)
		z = Bit(1024)
		self.assertGreater(x, y)
		self.assertEqual(x, z)
