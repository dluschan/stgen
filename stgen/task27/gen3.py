from itertools import product, combinations
from random import sample, randint, choices, shuffle
from math import gcd


def lcm(a, b):
	return a * b // gcd(a, b)


def _random_mod(p, q, count):
	"""должна возвращать список чисел, каждое из которых делится или не делится на p[i]."""
	d = 1
	n = []
	for a, x in zip(p, q):
		if x == '0':
			d = lcm(d, a)
		else:
			n.append(x)
	return [d * randint(1, 100) * n[0] + randint(1, n[0] - 1) for i in range(count)]

def random_mod(p, count):
	"""должна возвращать список чисел, каждое из которых делится или не делится на p[i]."""
	magic = 100
	k = 2 ** len(params)
	res = [[] for i in range(k)]
	for _ in range(k * len(p) * magic):
		x = randint(1, 10 ** 3)
		y = 0
		for q in p:
			y *= 2
			if x % q:
				y += 1
		res[y].append(x)
	assert all(res), "empty category: " + str(res)
	return [sample(x, min(len(x), count)) for x in res]

params = [7, 18]
m = 3
k = 2 ** len(params)
src = random_mod(params, 10)
pack = []
for i in range(m ** k):
	degree = []
	for _ in range(k):
		degree.append(i % m)
		i //= m
	if sum(degree) >= m - 1:
		r = []
		for x, y in zip(src, degree):
			r += choices(x, k=y)
		shuffle(r)
		pack.append(r)
for p in pack:
	print(f'"""{len(p)}')
	print(*p, sep='\n')
	print('""",')
