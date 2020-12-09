from .common import *
from random import choice


class Type5(Task12):
	def __init__(self):
		self.task = MaskedHostAddress()
		self.extreme = {max: ["наибольшее количество единиц", "наименьшее количество нулей"], min: ["наименьшее количество единиц", "наибольшее количество нулей"]}
		self.key = choice(list(self.extreme.keys()))
		self.fun = [lambda x: x, lambda x: 32 - x]
		self.digit = choice([0, 1])

	def category(self):
		return Task12.category(self) + 'Тип 5'

	def question_text(self):
		question = "Для узла с IP-адресом {host} адрес сети равен {network}. Определите какое {digits} может быть в маске сети.<br>Ответ запишите в виде десятичного числа."
		return Task12.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'network': self.latex(self.task.network()), 'digits': self.extreme[self.key][self.digit]})

	def question_answer(self):
		return self.fun[self.digit](self.key(self.task.suitable()).ones())
