def latex(s):
	return "\\( " + s + " \\)"


def get_factors(n):
	"""Возвращает отсортированный по возрастанию список натуральных делителей числа n."""
	head, tail, k = [], [], 1
	while k * k < n:
		if n % k == 0:
			head.append(k)
			tail.append(n // k)
		k += 1
	if k * k == n:
		head.append(k)
	return head + tail[::-1]


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


decimal_digits = '0123456789'
latin_alphabet_small   = 'abcdefghijklmnopqrstuvwxyz'
russian_alphabet_small = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
greek_alphabet_small   = 'αβγδεζηθικλμνξοπρστυφχψω'
latin_alphabet_big   = latin_alphabet_small.upper()
russian_alphabet_big = russian_alphabet_small.upper()
greek_alphabet_big   = greek_alphabet_small.upper()
hex_digits = decimal_digits + latin_alphabet_small[:6]
letters = latin_alphabet_small
