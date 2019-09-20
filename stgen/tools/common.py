letters = 'abcdefghijklmnopqrstuvwxyz'


def latex(s):
	return "\\( " + s + " \\)"


def get_primes(n):
	"""возвращает список из первых n простых чисел"""
	assert n > 0, "количество простых чисел должно быть больше нуля"
	primes = [2]

	for _ in range(n - 1):
		next = primes[-1] + 1
		while any(next % x == 0 for x in primes):
			next += 1
		primes.append(next)

	return primes
