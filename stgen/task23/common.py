from ..tools.task import BaseTask
from ..tools.systemeq import SystemEquation
from ..tools.boolequation import *


class Task23(BaseTask):
	"""ЕГЭ по информатике - Задача номер 23"""
	def __init__(self):
		super().__init__()
		self.question = '''Определите сколько существует различных наборов значений логических переменных {variables}, 
		которые удовлетворяют системе уравнений {equations}.'''

	def category(self):
		return super().category() + 'Задача 23/'

	def question_text(self):
		return self.question.format(variables=self.latex(''.join(sorted(map(str, self.system.terms)))), equations=self.system)

	def question_answer(self):
		return self.system.count()

	def question_type(self):
		return 'numerical'


class Homogeneous(Task23):
	"""Система однородных уравнений"""
	def __init__(self):
		super().__init__()
		s = self.step()
		self.system = SystemEquation([shift(self.template, dict(zip(s.keys(), map(lambda x: k*x, s.values())))) for k in range(self.eqcount())])

	def eqcount(self):
		n = randint(9, 10)
		return (n - len(terms(self.template))) // max(self.step().values()) + 1

	def step(self):
		return randint(1, len(min(analyze(self.template).values(), key=len)))
