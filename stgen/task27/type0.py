from .common import Task27
from random import randint


class Type0(Task27):
	def __init__(self):
		self.test_size = 5
		self.params = {
			'n': [int, [1, 10 ** 4], 'количество пар чисел'],
			's': [int, None, 'искомая сумма'],
			'a': [int, [1, 2 ** 30], 'первое число в паре'],
			'b': [int, [1, 2 ** 30], 'второе число в паре']
		}
		self.k = randint(2, 100)
		self.legend = f"""Имеется набор данных, состоящий из пар положительных целых чисел.
		Необходимо выбрать из каждой пары ровно одно число так, чтобы сумма всех выбранных
		чисел не делилась на {self.k} и при этом была максимально возможной.
		Если получить требуемую сумму невозможно, в качестве ответа нужно вывести 0."""
		self.solver = f"""k = {self.k}
n = int(input())
s = 0
r = None
for _ in range(n):
	a, b = map(int, input().split())
	s += max(a, b)
	if abs(a - b) % k != 0 and (r is None or abs(a - b) < r):
		r = abs(a - b)
if s % k == 0:
	if r:
		s -= k
	else:
		s = 0
print(s)
"""
		self.input_format = """n
a b|n"""
		self.output_format = """s"""
		self.input_samples = ["""5
34 89
1 88
32 34
5 7
12 17
"""]

	def category(self):
		return super().category() + 'Тип 0'

