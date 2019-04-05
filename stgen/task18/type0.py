from random import randint, shuffle
from functools import reduce
from intervals import closed, empty
from .common import *
from ..tools.common import letters
from ..tools.boolean import Membership, NotMembership, Disjunction


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
			self.segment_terms[Q] = (begin - left, begin + length + right)
			self.terms.append(NotMembership('x', Q))
			self.A &= closed(begin - left, begin + length + right)
		self.pos_right = randint(0, self.pos_amount)
		self.pos_left = self.pos_amount - self.pos_right
		self.P = []
		for P in self.segments_name[self.neg_amount:self.neg_amount + self.pos_right]:
			left = randint(0, 50)
			right = left + randint(0, 50)
			self.segment_terms[P] = (begin + length + left, begin + length + right)
			self.terms.append(Membership('x', P))
			self.A -= closed(begin + length + left, begin + length + right)
		for P in self.segments_name[self.neg_amount + self.pos_right:]:
			left = randint(0, 50)
			right = left + randint(0, 50)
			self.segment_terms[P] = (begin - right, begin - left)
			self.terms.append(Membership('x', P))
			self.A -= closed(begin - right, begin - left)
		shuffle(self.terms)
		self.system = reduce(Disjunction, self.terms)

	def category(self):
		return super().category() + 'Тип 0'

	def question_text(self):
		return self.question.format(
			segments=', '.join(map(
				lambda s: "{seg} = [{a}; {b}]".format(seg=s, a=self.segment_terms[s][0], b=self.segment_terms[s][1]),
				self.segment_terms)
			),
			expr=self.latex(repr(self.system))
		)

	def question_answer(self):
		return self.A.upper - self.A.lower

