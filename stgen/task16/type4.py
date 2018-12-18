from .common import *
from random import choices, sample


class Type4(Task16):
	"""Вычисления «в столбик» в разных системах счисления."""
	def __init__(self):
		super().__init__()
		self.question = "Значение выражения {expr} записали {base}. Определите сколько цифр {digit} содержится в этой записи."
		self.base = randint(2, 6)
		self.digit = choice([0, self.base - 1])
		self.head_count = randint(2, 4)
		self.tail_count = randint(1, 2)
		self.degree = choices(range(1, int(log(36, self.base)) + 1), k=self.head_count)
		self.head = sample(range(100, 1001), self.head_count)
		self.tail = sample(range(10, 1001), self.tail_count)
		self.head_sign = [randint(0, 1) for _ in range(self.head_count)]
		self.tail_sign = [randint(0, 1) for _ in range(self.tail_count)]
		self.head_number = sum([[-1, 1][self.head_sign[i]] * (self.base ** self.degree[i]) ** self.head[i] for i in range(self.head_count)])
		if self.head_number < 0:
			self.head_sign = [1-sign for sign in self.head_sign]
			self.head_number *= -1
		self.tail_number = sum([[-1, 1][self.tail_sign[i]] * self.tail[i] for i in range(self.tail_count)])
		if self.tail_number > 0:
			self.tail_sign = [1-sign for sign in self.tail_sign]
			self.tail_number *= -1
		while self.head_sign[0] == 0:
			self.head_sign.append(self.head_sign.pop(0))
			self.degree.append(self.degree.pop(0))
			self.head.append(self.head.pop(0))
		self.head_expr = ' '.join(['-+'[self.head_sign[i]] + ' ' + str(self.base ** self.degree[i]) + '^{' + str(self.head[i]) + '}' for i in range(self.head_count)])
		self.tail_expr = ' '.join(['-+'[self.tail_sign[i]] + ' ' + str(self.tail[i]) for i in range(self.tail_count)])

	def category(self):
		return super().category() + 'Тип 4/'

	def question_text(self):
		return self.question.format(
			expr=self.latex(self.head_expr[2:] + ' ' + self.tail_expr),
			base=self.notation(self.base),
			digit=self.latex(self.digits[self.digit])
		)

	def question_answer(self):
		return transform(self.head_number + self.tail_number, self.base).count(self.digits[self.digit])

