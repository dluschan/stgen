import unittest
from stgen.tools.systemeq import SystemEquation
from stgen.tools.boolean import *
from stgen.task23.compile import parse
from stgen.task23.type0 import Type0


class SystemEquationViewTest(unittest.TestCase):
	def test_term(self):
		self.assertEqual(repr(Variable('x1')), 'x_{1}')

	def test_true_const(self):
		self.assertEqual(str(TrueConst()), '1')

	def test_fasle_const(self):
		self.assertEqual(str(FalseConst()), '0')

	def test_negation(self):
		self.assertEqual(repr(Negation(Variable('x1'))), '\overline x_{1}')

	def test_implication(self):
		self.assertEqual(str(Implication(Variable('x1'), Variable('x2'))), 'x1 -> x2')
		self.assertEqual(repr(Implication(Variable('x1'), Variable('x2'))), 'x_{1} \implies x_{2}')

	def test_Term_Equal_True(self):
		self.assertEqual(repr(Equal(Variable('x1'), TrueConst())), 'x_{1} \\equiv 1')


class TestShift(unittest.TestCase):
	def test_shift(self):
		terms = [Variable('x1'), Variable('x1')]
		self.assertEqual(analyze(shift(Conjunction(terms[0], terms[1]), 1)), {'x': [2]})

	def test_shift_parse(self):
		self.assertEqual(analyze(shift(parse('x1 == x1'), 1)), {'x': [2]})


class SystemEquationTest(unittest.TestCase):
	def test_SystemEquation_with_shift(self):
		t = 'x1 -> x2'
		n = 5
		s = SystemEquation([shift(parse(t), k) for k in range(n)])
		self.assertEqual(s.count(), n + 1 + 1)

	def test_SystemEquation_fake(self):
		s = SystemEquation([parse('x1 & x2 -> y1 | z2 == 1'), parse('x1 & x6 -> y2 | z1 == 1'), parse('x1 & x3 -> y4 | z3 == x4')])
		self.assertEqual(s.count(), 904)

	def test_SystemEquation_repeate(self):
		s = SystemEquation([parse('x1 & x2 -> y1 | z2 == 1'), parse('x1 & x6 -> y2 | z1 == 1'), parse('x1 & x3 -> y4 | z3 == x4')])
		self.assertEqual(analyze(s.system), {'x': [1, 2, 6, 3, 4], 'y': [1, 2, 4], 'z': [2, 1, 3]})

	def test_SystemEquation_1(self):
		s = SystemEquation([parse('x1')])
		self.assertEqual(s.count(), 1)

	def test_SystemEquation_1d(self):
		s = SystemEquation([parse('x1'), parse('x2')])
		self.assertEqual(s.count(), 1)

	def test_SystemEquation_1t(self):
		s = SystemEquation([parse('x1 | x2'), parse('x2')])
		self.assertEqual(s.count(), 2)

	def test_SystemEquation_2(self):
		s = SystemEquation([parse('x1 == x2')])
		self.assertEqual(s.count(), 2)

	def test_SystemEquation_3(self):
		s = SystemEquation([parse('x1 -> x2')])
		self.assertEqual(s.count(), 3)

	def test_SystemEquation_simple(self):
		s = SystemEquation([parse('(x1 -> x2) & (x2 -> x3) & (y1 -> y2) & (y2 -> y3) == 1')])
		self.assertEqual(s.count(), 16)

	def test_SystemEquation(self):
		s = SystemEquation([parse('(x1 -> x2) & (y1 -> y2) == 1'), parse('(x2 -> x3) & (y2 -> y3) == 1')])
		self.assertEqual(s.count(), 16)


class EqualAnalyze(unittest.TestCase):
	def test_analyze(self):
		self.assertEqual(analyze(parse('x1 == x2')), {'x': [1, 2]})

	def test_shift_const(self):
		self.assertEqual(analyze(shift(parse('x1 == x2'), 2)), analyze(parse('x3 == x4')))

	def test_shift_var(self):
		self.assertEqual(analyze(shift(parse('(x1 == x2) & (y1 -> z1) == 1'), {'x': 2, 'y': 1, 'z': 1})), analyze(parse('(x3 == x4) & (y2 -> z2) == 1')))

	def test_shift_positive(self):
		self.assertEqual(analyze(shift(Positive(Variable('x1')), 1)), {'x': [2]})

	def test_save(self):
		eq = parse('x1 == x2')
		shift(eq, 1)
		self.assertEqual(analyze(eq), analyze(parse('x1 == x2')))

	def test_varlist(self):
		self.assertEqual(varlist(parse('x1 & x2 -> y1 | z2 == 1')), ['x1', 'x2', 'y1', 'z2'])


class Type0Test(unittest.TestCase):
	@unittest.skip("too long time, before need fix error in solver equition system module")
	def test_type0(self):
		self.assertEqual(type(Type0().question_answer()), int)


class BracedTest(unittest.TestCase):
	def test_1(self):
		self.assertEqual(str(parse('x1 & x2 | x3 == 1')), 'x1 & x2 | x3 == 1')
		self.assertEqual(repr(parse('x1 & x2 | x3 == 1')), 'x_{1} \\wedge x_{2} \\vee x_{3} \\equiv 1')

	def test_parse_and_print(self):
		self.assertEqual(str(parse('(x1 & x2) | x3 == 1')), '(x1 & x2) | x3 == 1')
		self.assertEqual(repr(parse('(x1 & x2) | x3 == 1')), '\\left( x_{1} \\wedge x_{2} \\right) \\vee x_{3} \\equiv 1')


if __name__ == "__main__":
	unittest.main()
