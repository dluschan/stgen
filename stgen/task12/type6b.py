from .common import *


class Type6b(Task12):
	def __init__(self):
		self.task = LimitMaskedHostAddressDeterminate()

	def category(self):
		return Task12.category(self) + 'Тип 6b'

	def question_text(self):
		question = "Для узла с IP-адресом {host} маска сети равна {netmask}. Определите какой номер по порядку имеет данный компьютер в сети.<br>Ответ запишите в виде десятичного числа."
		return Task12.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'netmask': self.latex(self.task.netmask())})

	def question_answer(self):
		return self.task.hostnumber()
