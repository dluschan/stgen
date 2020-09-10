from .common import Task27


class Type4(Task27):
	def __init__(self):
		super().__init__()
		self.test_size = 5
		self.params = {
			'a': [int, [1, 10000], 'левая граница отрезка'],
			'b': [int, [10001, 20000], 'правая граница отрезка'],
			'k': [int, [1, 10], 'количество различных натуральных делителей'],
			'n': [int, None, 'количество найденных чисел'],
			'm': [int, None, 'минимальное из найденных чисел'],
			's': [int, None, 'сумма всех различных натуральных делителей минимального найденного числа'],
		}
		self.legend = f"""Рассматриваются все натуральные числа на отрезке {self.latex("[a; b]")}. Найдите количество чисел, имеющих ровно {self.latex("k")} различных натуральных делителей, минимальное из них и сумму всех его делителей. Если на отрезке нет искомых чисел, то минимальное из искомых и сумма его делителей считается равными 0."""

		self.solver = """def get_factors(n):
	factors = []
	d = 1
	while d * d < n:
		if n % d == 0:
			factors.append(d)
			factors.append(n // d)
		d += 1
	if d * d == n:
		factors.append(d)
	return factors

a, b, k = map(int, input().split())
n, m, s = 0, 0, 0
#Порядок обхода важен для поиска минимума
for x in range(b, a - 1, -1):
	d = get_factors(x)
	if len(d) == k:
		n, m, s = n + 1, x, sum(d)
print(n, m, s)
"""
		self.input_format = """a b k"""
		self.output_format = """n m s"""
		self.input_samples = ["""134823 144498 6"""]

	def category(self):
		return super().category() + 'Тип 4'

