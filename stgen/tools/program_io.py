from .common import latex
from random import randint, uniform, expovariate


def parse_line(s, params):
	s = s.split("*")
	res = [params[p][2] + " " + latex(p) for p in s[0].split()]
	if len(res) > 1:
		res = res[:-2] + [res[-2] + " и " + res[-1]]
	res = ", ".join(res)
	if len(s) > 1:
		res = latex(s[1]) + " " + res
	return res + ". "


def parse_input(s, params):
	res = "<br>Формат входных данных<br>"
	p = s.split("\n")
	if len(p) == 0:
		res = "Программа не получает входные данные"
	elif len(p) == 1:
		s = p[0].split("|")
		end = ("В " + latex(s[1]) + " строках " if len(s) > 1 else "В единственной строке ") + "задаётся "
		res += end + parse_line(s[0], params)
	else:
		for i, s in enumerate(p):
			s = s.split("|")
			begin = "В "
			num = ["первой ", "первых "] if i == 0 else ["следующей ", "следующих "]
			end = (latex(s[1]) + " " + num[1] + "строках " if len(s) > 1 else num[0] + "строке ") + "задаётся "
			res += begin + end + parse_line(s[0], params)
	return res.strip()


def parse_output(s, params):
	res = "<br>Формат выходных данных<br>"
	p = s.split("\n")
	if len(p) == 0:
		res = "Программа не выводит данные"
	elif len(p) == 1:
		s = p[0].split("|")
		end = ("В " + latex(s[1]) + " строках выводятся " if len(s) > 1 else "В единственной строке выводится ")
		res += end + parse_line(s[0], params)
	else:
		for i, s in enumerate(p):
			s = s.split("|")
			begin = "В "
			num = ["первой ", "первых "] if i == 0 else ["следующей ", "следующих "]
			end = latex(s[1]) + (num[1] + " строках выводятся " if len(s) > 1 else num[0] + "строке выводится ")
			res += begin + end + parse_line(s[0], params)
	return res.strip()


def generate_item(x, params, generated):
	if params[x][0] == int:
		magic_const = 10
		generated[x] = max(min(params[x][1][1], int(expovariate(magic_const / params[x][1][1]))), params[x][1][0])
	elif params[x][0] == float:
		generated[x] = uniform(*params[x][1])
	elif params[x][0] == str:
		generated[x] = ""
	return generated[x]


def generate_line(s, params, generated):
	q = s.split("*")
	if len(q) > 1:
		return " ".join([str(generate_item(q[0], params, generated)) for _ in range(eval(q[1], generated))])
	else:
		return " ".join(str(generate_item(x, params, generated)) for x in q[0].split())


def generate_input(s, params):
	generated = {}
	res = ""
	for line in s.split("\n"):
		parts = line.split("|")
		if len(parts) > 1:
			for i in range(eval(parts[1], generated)):
				res += generate_line(parts[0], params, generated) + "\n"
		else:
			res += generate_line(parts[0], params, generated) + "\n"
	return res
