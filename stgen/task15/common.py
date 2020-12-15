from random import choice, randint, sample, shuffle
from pydot import graph_from_dot_data
from pygraph.classes.digraph import digraph
from pygraph.readwrite import dot
from ..tools.task import BaseTask


def horizontal(x):
	""""Функция устанавливает горизонтальные (т.е. между вершинами одного слоя) связи в графе"""
	k = randint(1, (len(x) + 1) // 2)
	for i in sample(range(len(x) - 1), k):
		yield (x[i], x[i + 1])


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


def graph(nodes):
	""""Функция генерирует направленный граф из списка вершин"""
	g = digraph()
	g.add_nodes(nodes)
	k = randint(3, (len(nodes) + 2) // 3)
	levels = [nodes[:1], *distribution(nodes[1:-1], k), nodes[-1:]]
	for i in range(len(levels) - 1):
		if len(levels[i]) >= 2:
			for edge in horizontal(levels[i]):
				g.add_edge(edge)
		for edge in addition(levels[i][:], levels[i+1][:]):
			g.add_edge(edge)
	return g


def dot_graph(g):
	"""Конвертирует граф в формат dot"""
	graph_dot = graph_from_dot_data(dot.write(g))[0]
	graph_dot.set_rankdir('LR')
	for node in graph_dot.get_nodes():
		node.set_shape('circle')
	return graph_dot


def solve(graph, start, end):
	"""Функция подсчитывает количество путей в графе"""
	if start == end:
		return 1
	else:
		return sum([solve(graph, start, finish) for finish in graph.incidents(end)])


def dot_to_svg(g):
	return dot_graph(g).create(format='svg').decode('utf-8')


class Task15(BaseTask):
	"""Поиск количества путей на графе."""
	def __init__(self):
		self.n = randint(10, 18)
		self.nodes = 'ДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'[:self.n]
		self.g = graph(list(self.nodes))
		self.question = """На рисунке - схема дорог, связывающих города {cites}.
			По каждой дороге можно двигаться только в одном направлении, указанном стрелкой.
			Сколько существует различных путей из города {begin} в город {end}? {graph}"""

	def category(self):
		return super().category() + 'Задача 15/'

	def question_text(self):
		return self.question.format(cites=', '.join(self.nodes), begin=self.nodes[0], end=self.nodes[-1], graph=dot_to_svg(self.g))

	def question_answer(self):
		return solve(self.g, self.nodes[0], self.nodes[-1])

	def question_type(self):
		return 'numerical'

	def cdata(self):
		return True
