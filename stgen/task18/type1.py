from random import randint, shuffle, choice
from math import lcm
from .common import *
from ..tools.common import letters
from ..tools.boolean import Conjunction, Disjunction, mutation, brackets, Divisibility, Equal, TrueConst, Negation


class Type1(Task18):
	"""Определение искомого делителя.
	(not x % B) || (not x % C) || (x % A) == 1; A == divisor(least_common_multiple(B, C))
	((not x % B) && (not x % C)) || (x % A) == 1; A == common_divisor(B, C)
	(x % B) || (x % C) || (not x % A) == 1; A == multiple(B) || multiple(C)
	(not x % B) || (x % C) || (not x % A) == 1; A == multiple(C // z), z: gcd(z, C // gcd(B, C)) == 1
	"""
	def __init__(self):
		super().__init__()
		self.unknown_var = letters.upper()[0]
		self.var_name = "x"
		self.question = """Определите {extrem_type} значение натурального числа {unknown_var}, 
		что выражение {expr} истинно при любом значении переменной {var_name}."""

	def category(self):
		return super().category() + 'Тип 1/'

	def question_text(self):
		return self.question.format(
			expr=self.latex(repr(brackets(self.fun))),
			extrem_type=self.extrem_type,
			unknown_var=self.latex(self.unknown_var),
			var_name=self.latex(self.var_name)
		)

	def question_answer(self):
		return self.ans


class SubTypeA(Type1):
	def __init__(self):
		super().__init__()
		self.B = randint(2, 99)
		self.C = randint(3, 97)
		self.extrem_type = "максимальное"
		self.fun = Equal(Disjunction(Disjunction(Negation(Divisibility(self.var_name, str(self.B))), Negation(Divisibility(self.var_name, str(self.C)))), Divisibility(self.var_name, self.unknown_var)), TrueConst())
		self.ans = lcm(self.B, self.C)

	def category(self):
		return super().category() + 'Подтип A'
