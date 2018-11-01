import unittest
from use.tools.ip import *


class TestIPv4(unittest.TestCase):
	def test_Address(self):
		a = Address(200 * 256**3 + 129 * 256**2 + 240 * 256**1 + 55 * 256**0)
		self.assertEqual(str(a), '200.129.240.55')
		self.assertTrue(a[3] == 200 and a[2] == 129 and a[1] == 240 and a[0] == 55)

	def test_NetworkMask(self):
		m = NetworkMask(10)
		self.assertEqual(str(m), '255.192.0.0')

	def test_NetworkAddress(self):
		a = HostAddress(3221226219)
		m = NetworkMask(26)
		self.assertEqual(str(a & m), '192.0.2.192')

	def test_TripleIPAddressesDeterminate(self):
		for _ in range(100):
			self.assertEqual(len(MaskedHostAddressDeterminate().suitable()), 1)

	def test_LimitMaskedHostAddressDeterminate(self):
		for _ in range(100):
			self.assertLess(LimitMaskedHostAddressDeterminate().network_mask.zeros(), 17)
