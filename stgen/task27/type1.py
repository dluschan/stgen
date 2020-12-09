from .common import Task27
from random import sample
from ..tools.common import get_primes


class Type1(Task27):
	def __init__(self):
		super().__init__()
		self.test_size = 5
		self.params = {
			'n': [int, [1, 10], 'количество чисел'],
			'x': [int, [1, 10 ** 4], 'натуральное число'],
			'r': [int, None, 'искомое контролькое значение'],
		}
		a, b = sample(get_primes(10), 2)
		self.legend = f"""Для последовательности из n натуральных чисел нужно посчитать контрольное значение, 
равное наибольшему произведению двух её элементов, которое кратно {a*b}, или равное нулю, если такой пары чисел
в последовательности нет."""
		self.solver = f"""a = {a}
b = {b}
n = int(input())
ma, mb, mab, mab2, mn = [0] * 5
for _ in range(n):
	x = int(input())
	if	 x % a == 0 and x % b == 0:
		if x > mab:
			mab, mab2 = x, mab
		elif x > mab2:
			mab2 = x
	elif x % a == 0 and x % b != 0:
		if x > ma:
			ma = x
	elif x % a != 0 and x % b == 0:
		if x > mb:
			mb = x
	elif x % a != 0 and x % b != 0:
		if x > mn:
			mn = x
print(max(ma * mb, mab * max(ma, mb, mab2, mn)))
"""
		self.input_format = """n
x|n"""
		self.output_format = """r"""
		self.input_samples = ["""5
40
1000
7
28
55
"""]

	def category(self):
		return super().category() + 'Тип 1'

