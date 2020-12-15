from random import randint
from pydot import graph_from_dot_data
from pygraph.classes.digraph import digraph
from pygraph.readwrite import dot
from ..tools.task import BaseTask
from ..tools.list_tools import pairs, split, align


def graph(nodes):
	""""Функция генерирует направленный граф из списка вершин"""
	g = digraph()
	g.add_nodes(nodes)
	k = randint(3, (len(nodes) + 2) // 3)
	levels = [nodes[:1], *split(nodes[1:-1], k), nodes[-1:]]
	for i in range(len(levels) - 1):
		if len(levels[i]) >= 2:
			for edge in pairs(levels[i], randint(1, (len(levels[i]) + 1) // 2)):
				g.add_edge(edge)
		for edge in zip(*align(levels[i], levels[i+1])):
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
