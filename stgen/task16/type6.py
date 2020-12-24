from .common import *
from ..tools.decompose import single_decompose


class Type6(Task16):
	"""Использование сдвига вместо деления и умножения."""
	def __init__(self):
		super().__init__()
		self.question = 'Найдите значение выражения {expression}. Ответ запишите в системе счисления с основанием {base}.'
		self.m = randint(10, 12)
		self.k = randint(2, 4)
		self.m = single_decompose(self.m, self.k, 6)
		self.source_base = randint(2, 9)
		self.limit_base = {2: 5, 3: 3, 4: 2, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1}
		self.limit_factor = {2: 8, 3: 5, 4: 4, 5: 3, 6: 3, 7: 3, 8: 2, 9: 2}
		self.target_base = self.source_base ** randint(1, self.limit_base[self.source_base])
		self.terms = [
			[
				randint(10**(m-1), 10**(m+1)),
				randint(1, self.limit_base[self.source_base]),
				randint(2, self.limit_factor[self.source_base]),
				choice([self.div, self.prod]),
				choice([+1, -1])
			] for m in self.m
		]
		for i in range(self.k):
			if self.terms[i][3] == self.prod:
				self.terms[i][0] = self.terms[i][0] // (self.source_base ** self.terms[i][2]) * (self.source_base ** self.terms[i][2])
		if self.value(self.terms) < 0:
			self.terms = [[term[0], term[1], term[2], term[3], -term[4]] for term in self.terms]
		while self.terms[0][4] < 0:
			self.terms.append(self.terms.pop(0))

	def category(self):
		return super().category() + 'Тип 6'

	def question_text(self):
		expression = ' '.join([self.convert(*p, self.source_base) for p in self.terms])[2:]
		return self.question.format(expression=self.latex(expression), base=self.latex(self.target_base))

	@staticmethod
	def div(x, k, base):
		return x * (base ** k) + randint(0, base ** k - 1)

	@staticmethod
	def prod(x, k, base):
		return x // (base ** k)

	def convert(self, x, m, k, f, s, base):
		sings = {+1: '+ ', -1: '- ', self.div: ' \\div ', self.prod: ' \\times '}
		params = ['\\text' + '{' + transform(f(x, k, base), base ** m) + '}' + '_' + '{' + str(base**m) + '}', str(base**k)]
		if f == self.div:
			return sings[s] + self.floor(sings[f].join(params))
		else:
			return sings[s] + sings[f].join(params)

	@staticmethod
	def floor(expr):
		return ' \\lfloor ' + expr + ' \\rfloor '

	@staticmethod
	def value(terms):
		return sum([p[0] * p[4] for p in terms])

	def question_answer(self):
		return transform(self.value(self.terms), self.target_base)
