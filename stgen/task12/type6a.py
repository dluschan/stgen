from .common import *


class Type6a(Task12):
	def __init__(self):
		self.task = LimitMaskedHostAddressDeterminate()

	def category(self):
		return Task12.category(self) + 'Тип 6a'

	def question_text(self):
		question = "Для узла с IP-адресом {host} адрес сети равен {network}. Определите какой номер по порядку имеет данный компьютер в сети.<br>Ответ запишите в виде десятичного числа."
		return Task12.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'network': self.latex(self.task.network())})

	def question_answer(self):
		return self.task.hostnumber()
