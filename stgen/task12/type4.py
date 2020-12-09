from .common import *
from random import choice


class Type4(Task12):
	def __init__(self):
		self.task = MaskedHostAddress()
		self.extreme = {max: 'наибольшее', min: 'наименьшее'}
		self.order = [["первый слева", "четвёртый справа"], ["второй слева", "третий справа"], ["третий слева", "второй справа"], ["четвёртый слева", "первый справа"]]
		self.byte = (self.task.netmask().ones() - 1) // 8
		self.key = choice(list(self.extreme.keys()))

	def category(self):
		return Task12.category(self) + 'Тип 4'

	def question_text(self):
		question = "Для узла с IP-адресом {host} адрес сети равен {network}. Определите какое {extreme} значение может принимать {order} байт в маске сети.<br>Ответ запишите в виде десятичного числа."
		return Task12.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'network': self.latex(self.task.network()), 'extreme': self.extreme[self.key], 'order': choice(self.order[self.byte])})

	def question_answer(self):
		return self.key(self.task.suitable())[3 - self.byte]
