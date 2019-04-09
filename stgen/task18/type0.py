from random import randint, shuffle, choice
from functools import reduce
from intervals import closed, empty, inf
from .common import *
from ..tools.common import letters
from ..tools.boolean import Membership, NotMembership, Disjunction, cnf
from ..tools.choices import choices
from ..tools.boolequation import random_function


class Type0(Task18):
	"""Определение искомого отрезка."""
	def __init__(self):
		super().__init__()
		self.question = """На числовой прямой даны отрезки: {segments}.
		Определите наименьшую длину такого отрезка A, что выражение {expr} истинно при любом значении переменной х."""
		begin = randint(-100, 100)
		length = randint(5, 50)
		self.segments_amount = randint(2, 5)
		self.segments_name = list(letters.upper()[1:])
		shuffle(self.segments_name)
		self.segments_name = self.segments_name[:self.segments_amount]
		self.terms = [Membership('x', 'A')]
		self.neg_amount = randint(1, self.segments_amount)
		self.pos_amount = self.segments_amount - self.neg_amount
		self.segment_terms = {}
		self.A = ~empty()
		self.Q = []
		for Q in self.segments_name[:self.neg_amount]:
			left = randint(0, 50)
			right = randint(0, 50)
			self.segment_terms[Q] = closed(begin - left, begin + length + right)
			self.terms.append(NotMembership('x', Q))
			self.A &= closed(begin - left, begin + length + right)
		self.pos_right = randint(0, self.pos_amount)
		self.pos_left = self.pos_amount - self.pos_right
		self.P = []
		for P in self.segments_name[self.neg_amount:self.neg_amount + self.pos_right]:
			left = randint(0, 50)
			right = left + randint(0, 50)
			self.segment_terms[P] = closed(begin + length + left, begin + length + right)
			self.terms.append(Membership('x', P))
			self.A -= closed(begin + length + left, begin + length + right)
		for P in self.segments_name[self.neg_amount + self.pos_right:]:
			left = randint(0, 50)
			right = left + randint(0, 50)
			self.segment_terms[P] = closed(begin - right, begin - left)
			self.terms.append(Membership('x', P))
			self.A -= closed(begin - right, begin - left)
		shuffle(self.terms)
		self.system = reduce(Disjunction, self.terms)

	def category(self):
		return super().category() + 'Тип 0'

	def question_text(self):
		return self.question.format(
			segments=', '.join(s + ' = ' + str(self.segment_terms[s]) for s in self.segment_terms),
			expr=self.latex(repr(self.system))
		)

	def question_answer(self):
		return self.A.upper - self.A.lower


class Type1(Task18):
	"""Определение искомого отрезка."""
	def random_segment(self):
		dot_limits = (-100, 100)
		if randint(1, 100) < 10:
			beam = closed(randint(*dot_limits), inf)
			if randint(0, 1):
				return beam
			else:
				return ~beam
		else:
			a, b = randint(*dot_limits), randint(*dot_limits)
			return closed(*sorted(a, b))

	def __init__(self):
		super().__init__()
		self.question = """На числовой прямой даны отрезки: {segments}.
		Определите наименьшую длину такого отрезка A, что выражение {expr} истинно при любом значении переменной х."""
		#1 выбрать имя искомого отрезка
		unknown = letters.upper()[0]
		var_name = 'x'

		#2 выбрать имена всем интервалам
		segment_amount = randint(2, 10)
		segments_name = list(letters.upper()[1:])
		shuffle(segments_name)
		segments_name = segments_name[:segment_amount]

		#3 по точкам сгенерировать интервалы: отрезки и лучи
		segments = [[name, self.random_segment()] for name in segments_name]

		#4 сгенерировать для каждого интервала соответствующий терм принадлежности
		term_amount = randint(2, 10)
		terms = [[segment_name, segment, [Membership, NotMembership].choice()(var_name, segment_name)]
			for segment_name, segment in choices(segments, k=term_amount)]
		terms.append([])

		#5 сгенерировать случайную функцию от термов
		fun = random_function((t[2] for t in terms))
		norm_fun = cnf(fun)

		#6 вычислить X, Y и Z
		# if Z != 0:
		# 	res = "нужного A не существует"
		# else:
		# 	if X is limited and Y is limited and:
		# 		res = "какая наименьшая длина A"
		# 	if X is limited and Y not is limited and:
		# 		res = "какая наибольшая длина A" | "какая наименьшая длина A"
		# 	if X not is limited and Y is limited and:
		# 		X, Y = Y, X
		# 		res = "какая наибольшая длина A" | "какая наименьшая длина A"
		# 	if X not is limited and Y not is limited and:
		# 		res = "какая наибольшая длина A"


	def category(self):
		return super().category() + 'Тип 1'

	def question_text(self):
		return self.question.format(
			segments=', '.join(s + ' = ' + str(self.segment_terms[s]) for s in self.segment_terms),
			expr=self.latex(repr(self.system))
		)

	def question_answer(self):
		return self.A.upper - self.A.lower


