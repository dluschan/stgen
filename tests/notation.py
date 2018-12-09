import unittest
from stgen.tools.notation import transform

class TestTransform(unittest.TestCase):
    '''Тестирование перевода чисел в разные системы счисления.'''
    def test_transform(self):
        self.assertEqual(transform(255, 2), '11111111')

    def test_transform_abc(self):
        self.assertEqual(transform(255, 2, 'qw'), 'wwwwwwww')

    def test_transform_based(self):
        self.assertEqual(transform(255, 2, based = True), '11111111_{2}')

    def test_transform_error(self):
        self.assertRaises(IndexError, transform, 255, 2, 'q')
