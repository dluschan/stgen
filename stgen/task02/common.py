from ..tools.task import BaseTask
from ..tools.boolean import *
from ..tools.boolequation import random_function
from random import randint


class Task02(BaseTask):
	"""ЕГЭ по информатике - Задача номер 2"""
	def __init__(self):
		self.var_count = randint(3, 8)
		self.fun_count = randint(4, 4)
		self.vars = [Variable('x' + str(i)) for i in range(1, self.var_count + 1)]
		self.funs = [random_function(self.vars) for _ in range(4)]
		self.x = 1