from .common import latex


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
	res = "Формат входных данных\n"
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
	res = "Формат выходных данных\n"
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

