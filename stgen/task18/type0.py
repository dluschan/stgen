from random import randint, shuffle, choice
from functools import reduce
from intervals import open, closed, openclosed, closedopen, empty, inf
from .common import *
from ..tools.common import letters
from ..tools.boolean import Membership, NotMembership, Conjunction, Disjunction, cnf, get_disjunctions_from_conjuction, get_primary_terms_from_disjunctios
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
	def random_interval(self, a=-100, b=100):
		return choices((self.random_segment, self.random_beam, self.unbounded_interval), (85, 10, 5), k=1)[0](a, b)

	def random_beam(self, a=-100, b=100):
		return choice(self.random_left_beam, self.random_right_beam)(a, b)

	def random_left_beam(self, a=-100, b=100):
		return openclosed(-inf, randint(a, b))

	def random_right_beam(self, a=-100, b=100):
		return closedopen(randint(a, b), inf)

	def unbounded_interval(self):
		return open(-inf, inf)

	def random_segment(self, a=-100, b=100):
		return closed(*sorted((randint(a, b), randint(a, b))))

	def random_left_segment(self, a):
		return choices((self.random_segment, self.random_left_beam), (90, 10), k=1)[0](a - 101, a - 1)

	def random_right_segment(self, a):
		return choices((self.random_segment, self.random_right_beam), (90, 10), k=1)[0](a + 1, a + 101)

	def random_not_intersect_segment(self, other):
		if other.lower == -inf and other.upper == inf:
			return empty()
		elif other.lower == -inf:
			return self.random_interval(other.upper + 1, other.upper + 101) - other
		elif other.upper == inf:
			return self.random_interval(other.lower - 101, other.lower - 1) - other
		else:
			return choice((self.random_left_segment(other.lower), self.random_right_segment(other.upper)))

	def __init__(self):
		super().__init__()
		self.question = """На числовой прямой даны отрезки: {segments}."""

		#1 выбрать имя искомого отрезка
		unknown = letters.upper()[0]
		var_name = 'x'

		#2 выбрать имена всем интервалам
		segment_amount = randint(2, 10)
		segments_name = list(letters.upper()[1:])
		shuffle(segments_name)
		regular_segments_name = segments_name[:segment_amount]
		extra_segments_name = segments_name[segment_amount:]

		#3 по точкам сгенерировать интервалы: отрезки и лучи
		regular_segments = [[name, self.random_segment()] for name in regular_segments_name]

		#4 сгенерировать для каждого интервала пару соответствующих термов принадлежности
		regular_terms = [[segment_name, segment, membertype(var_name, segment_name)]
			for membertype in [Membership, NotMembership] for segment_name, segment in regular_segments]
		term_amount = randint(2, 10)

		#5 сгенерировать случайную функцию от термов
		self.used_terms = choices(regular_terms, k=term_amount)
		self.used_segments = {t[0]: t[1] for t in self.used_terms}
		self.extra_segments = {}
		extra_terms = []
		x, y = empty(), empty()
		self.fun = []
		for i in range(randint(2, 4)):
			u = choice([Membership, NotMembership])(var_name, unknown)
			w = [u]
			res_seg = ~empty()
			for j in range(randint(2, 4)):
				term = choice(self.used_terms)
				w.append(term[2])
				res_seg &= term[1] if type(term[2]) == NotMembership else ~term[1]
			if type(u) == NotMembership:
				z = x.to_atomic() & (res_seg | y)
				assert z.lower != -inf and z.upper != inf, "Failed x range"
				if not z.is_empty():
					extra_segment = self.random_not_intersect_segment(z)
					extra_name, *extra_segments_name = extra_segments_name
					self.extra_segments[extra_name] = extra_segment
					extra_terms.append([extra_name, extra_segment, NotMembership(var_name, extra_name)])
					w.append(extra_terms[-1][2])
					res_seg &= extra_segment
				y |= res_seg
			else:
				if res_seg.lower == -inf or res_seg.upper == inf:
					extra_segment = self.random_segment()
					extra_name, *extra_segments_name = extra_segments_name
					self.extra_segments[extra_name] = extra_segment
					extra_terms.append([extra_name, extra_segment, NotMembership(var_name, extra_name)])
					w.append(extra_terms[-1][2])
					res_seg &= extra_segment
				z = (x | res_seg).to_atomic() & y
				assert z.lower != -inf and z.upper != inf, "Failed x range"
				if not z.is_empty():
					extra_segment = self.random_not_intersect_segment(z)
					extra_name, *extra_segments_name = extra_segments_name
					self.extra_segments[extra_name] = extra_segment
					extra_terms.append([extra_name, extra_segment, NotMembership(var_name, extra_name)])
					w.append(extra_terms[-1][2])
					res_seg &= extra_segment
				x |= res_seg
				assert x.lower != -inf and x.upper != inf, "Failed x range"
			self.fun.append(w)
		self.fun = reduce(Conjunction, [reduce(Disjunction, [t for t in c]) for c in self.fun])
		assert x.lower != -inf and x.upper != inf, "Failed segment"
		if y.lower == -inf and y.upper == inf:
			if x.is_empty():
				self.ans = max(map(lambda s: s.upper - s.lower, (p for p in ~y)))
			else:
				self.ans = max(map(lambda s: s.upper - s.lower, (p for p in ~y if not (p & x).is_empty())))
			self.question += """
			Определеите максимальную длину такого отрезка A, что выражение {expr} истинно при любом значении переменной х.
			"""
		else:
			self.ans = 0 if x.is_empty() else x.upper - x.lower
			self.question += """
			Определеите минимальную длину такого отрезка A, что выражение {expr} истинно при любом значении переменной х.
			"""
		self.used_segments.update(self.extra_segments)

	def category(self):
		return super().category() + 'Тип 1'

	def question_text(self):
		return self.question.format(
			segments=self.latex((', '.join(s + ' = ' + str(self.used_segments[s]) for s in self.used_segments))),
			expr=self.latex(repr(self.fun))
		)

	def question_answer(self):
		return self.ans


