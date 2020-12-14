from random import randint, choice, shuffle
import pydot
from ..tools.task import BaseTask


def horizontal(x):
	""""Функция устанавливает горизонтальные (т.е. между вершинами одного слоя) связи в графе"""
	k = randint(1, (len(x) + 1) // 2)
	hor = set()
	while len(hor) < k:
		hor.add(choice(x[:-1]))
	res = []
	for w in hor:
		res.append((w, w+1))
	return res


def distribution(a, b):
	""""Функция разбивает список a на b промежутков"""
	e = list(range(2, len(a) - 1))
	assert(len(e) >= b - 1)
	shuffle(e)
	s = sorted(e[:b - 1] + [0] + [len(a)])
	r = []
	for i in range(b):
		r.append(a[s[i]: s[i+1]])
	return r


def addition(x, y):
	"""Функция получает два списка и расширяет меньший из них с помощью дубликатов его элементов,
	чтобы списки сравнялись по длине"""
	if len(x) < len(y):
		a, b = x, y
		r = False
	else:
		a, b = y, x
		r = True
	c = []
	while len(a) + len(c) < len(b):
		c.append(choice(a))
	a += c
	a.sort()
	if r:
		a, b = b, a
	return list(zip(a, b))


def graph(n):
	""""Функция генерирует граф заданной длины из набора вершин в виде списка пар вершин"""
	k = randint(3, (n + 2) // 3)
	levels = [[0], *distribution(list(range(1, n - 1)), k), [n - 1]]
	res = []
	for i in range(len(levels) - 1):
		if len(levels[i]) >= 2:
			res += horizontal(levels[i][:])
		res += addition(levels[i][:], levels[i+1][:])
	return res


def dot_graph(g, s):
	"""Конвертирует граф в формат dot с переименованием вершин согласно строке s"""
	graph = pydot.Dot(graph_type='digraph', rankdir='LR')
	node = pydot.Node('node')
	node.set("shape", 'circle')
	graph.add_node(node)
	for a, b in g:
		graph.add_edge(pydot.Edge(s[a], s[b]))
	return graph


def dict_graph(links):
	"""Функция преобразовывает граф из списка связей в список списков"""
	res = {}
	for key in set([x[0] for x in links] + [x[1] for x in links]):
		res[key] = [y[0] for y in filter(lambda x: x[1] == key, links)]
	return res


def solve(links, start, end):
	"""Функция подсчитывает количество путей в графе"""
	if start == end:
		return 1
	else:
		return sum([solve(links, start, finish) for finish in links[end]])


def dot(g, s):
	return dot_graph(g, s).create(format='svg').decode('utf-8')


class Task15(BaseTask):
	"""Поиск количества путей на графе."""
	def __init__(self):
		self.s = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
		self.n = randint(10, 18)
		self.g = graph(self.n)
		self.question = """На рисунке - схема дорог, связывающих города {cites}.
			По каждой дороге можно двигаться только в одном направлении, указанном стрелкой.
			Сколько существует различных путей из города {begin} в город {end}? {graph}"""

	def category(self):
		return super().category() + 'Задача 15/'

	def question_text(self):
		return self.question.format(cites=', '.join(self.s[:self.n]), begin=self.s[0], end=self.s[self.n-1], graph=dot(self.g, self.s))

	def question_answer(self):
		return solve(dict_graph(self.g), 0, self.n - 1)

	def question_type(self):
		return 'numerical'

	def cdata(self):
		return True
