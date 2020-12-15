from random import randint, shuffle, choice, choices
from functools import reduce
from intervals import open, closed, openclosed, closedopen, empty, inf
from .common import *
from ..tools.common import letters
from ..tools.boolean import Membership, NotMembership, Conjunction, Disjunction, mutation, brackets


class Type0(Task18):
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
		self.question = """На числовой прямой даны отрезки: {segments}.
		Определеите {extrem_type} длину такого отрезка {unknown_segment}, 
		что выражение {expr} истинно при любом значении переменной {var_name}."""

		#1 выбрать имя искомого отрезка
		self.unknown_segment = letters.upper()[0]
		self.var_name = "x"

		#2 выбрать имена всем интервалам
		segment_amount = randint(2, 10)
		segments_name = list(letters.upper()[1:])
		shuffle(segments_name)
		regular_segments_name = segments_name[:segment_amount]
		extra_segments_name = segments_name[segment_amount:]

		#3 сгенерировать интервалы
		regular_segments = [[name, self.random_segment()] for name in regular_segments_name]

		#4 сгенерировать для каждого интервала пару соответствующих термов принадлежности
		regular_terms = [[segment_name, segment, membertype(self.var_name, segment_name)]
			for membertype in [Membership, NotMembership] for segment_name, segment in regular_segments]
		term_amount = randint(3, 10)

		#5 сгенерировать случайную функцию от термов
		shuffle(regular_terms)
		regular_terms = regular_terms[:term_amount]

		self.used_segments = {}
		extra_terms = []
		x, y = empty(), empty()
		self.fun = []
		factors = randint(2, 3)
		for i in range(factors):
			u = choice([Membership, NotMembership])(self.var_name, self.unknown_segment)
			w = [u]
			res_seg = ~empty()
			shuffle(regular_terms)
			factor_lenght = randint(2, 8 // factors)
			for term in regular_terms[:factor_lenght]:
				self.used_segments[term[0]] = term[1]
				w.append(term[2])
				res_seg &= term[1] if type(term[2]) == NotMembership else ~term[1]
			if type(u) == NotMembership:
				z = x.to_atomic() & (res_seg | y)
				assert z.lower != -inf and z.upper != inf, "Failed x range"
				if not z.is_empty():
					extra_segment = self.random_not_intersect_segment(z)
					extra_name, *extra_segments_name = extra_segments_name
					self.used_segments[extra_name] = extra_segment
					extra_terms.append([extra_name, extra_segment, NotMembership(self.var_name, extra_name)])
					w.append(extra_terms[-1][2])
					res_seg &= extra_segment
				y |= res_seg
			else:
				if res_seg.lower == -inf or res_seg.upper == inf:
					extra_segment = self.random_segment()
					extra_name, *extra_segments_name = extra_segments_name
					self.used_segments[extra_name] = extra_segment
					extra_terms.append([extra_name, extra_segment, NotMembership(self.var_name, extra_name)])
					w.append(extra_terms[-1][2])
					res_seg &= extra_segment
				z = (x | res_seg).to_atomic() & y
				assert z.lower != -inf and z.upper != inf, "Failed x range"
				if not z.is_empty():
					extra_segment = self.random_not_intersect_segment(z)
					extra_name, *extra_segments_name = extra_segments_name
					self.used_segments[extra_name] = extra_segment
					extra_terms.append([extra_name, extra_segment, NotMembership(self.var_name, extra_name)])
					w.append(extra_terms[-1][2])
					res_seg &= extra_segment
				x |= res_seg
				assert x.lower != -inf and x.upper != inf, "Failed x range"
			shuffle(w)
			self.fun.append(w)
		self.fun = reduce(Conjunction, [mutation(reduce(Disjunction, [t for t in c])) for c in self.fun])
		assert x.lower != -inf and x.upper != inf, "Failed segment"
		if y.lower == -inf and y.upper == inf and y != ~empty():
			if x.is_empty():
				self.ans = max(map(lambda s: s.upper - s.lower, (p for p in ~y)))
			else:
				self.ans = max(map(lambda s: s.upper - s.lower, (p for p in ~y if not (p & x).is_empty())))
			self.extrem_type = "максимальную"
		else:
			self.ans = 0 if x.is_empty() else x.upper - x.lower
			self.extrem_type = "минимальную"

	def category(self):
		return super().category() + 'Тип 0'

	def question_text(self):
		return self.question.format(
			segments=self.latex((', '.join(s + ' = ' + str(self.used_segments[s]) for s in self.used_segments))),
			expr=self.latex(repr(brackets(self.fun))),
			extrem_type=self.extrem_type,
			unknown_segment=self.latex(self.unknown_segment),
			var_name=self.latex(self.var_name)
		)

	def question_answer(self):
		return self.ans


