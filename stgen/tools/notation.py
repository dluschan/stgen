def transform(x, n, digits='0123456789abcdefghijklmnopqrstuvwxyz', based=False):
	"""Возвращает строковое представление числа x в системе счисления n.

	Необязательный параметр digits задаёт цифры, используемые для представления числа, по умолчанию используются арабские
	цифры и маленькие буквы латинского алфавита. Если необязательный параметр based равен True, то основание выходной
	системы счисления добавляется к результирующей строке через нижние подчёркивание, значение по умолчанию False."""
	result = ''
	while x:
		result = digits[x % n] + result
		x //= n
	if based:
		result += '_' + '{' + str(n) + '}'
	return result


if __name__ == "__main__":
	s = input('Enter source number and its radix [optional]: ')
	if len(s.split()) == 1:
		x = int(s)
	elif len(s.split()) == 2:
		x, base = s.split()
		x = int(x, int(base))
	else:
		raise RuntimeError("Expected one or two parameters!")

	s = input('Enter target radix and desired digit [optional]: ')
	if len(s.split()) == 1:
		n, k = int(s), None
	elif len(s.split()) == 2:
		n, k = s.split()
		n = int(n)
	else:
		raise RuntimeError("Expected one or two parameters!")

	y = transform(x, n)
	print('Source number in target radix is {}.'.format(y))
	if k is not None:
		print('Desired digit met {} times'.format(y.count(k)))
