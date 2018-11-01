from .common import *
from ..tools.boolean import BinaryLogicOperation, Conjunction, Disjunction, Implication, Equal, Notequal, Negation, Brackets
from ..tools.common import letters
from random import choice, shuffle


class Type0(Homogeneous):
	"""Система логических уравнений, в решении которой лежит идея «битовых цепочек».

	На одном из этапов решения задача должна свестись к построению таблицы истанности с помощью инварианта
	«после единицы стоят только единицы» или «после нуля стоят только нули».
	Перед построением данной таблицы необходимо выполнить замену.
	x1 -> x2 == 1
	!x1 | x2 == 1
	x1 & !x2 == 0"""
	def __init__(self):
		capacity = randint(1, 6)
		family = randint(1, min(capacity, 3))
		unique = randint(family, min(capacity, 4))
		self.unique_terms = random_unique_terms(random_family(family), unique)
		template_terms = random_extended_terms(self.unique_terms, capacity)
		left = random_function(compile_terms(template_terms))
		right = shift(left, self.unique_terms)
		self.template = self.equation([left, right])
		super().__init__()

	@staticmethod
	def equation(args):
		view = choice([
			[Implication, [Positive, Positive], 1],
			[Disjunction, [Negation, Positive], 1],
			[Conjunction, [Negation, Positive], 0]
		])
		res = choice([
			[[Equal, FalseConst], [Equal, TrueConst]],
			[[Notequal, TrueConst], [Notequal, FalseConst]],
		])[view[2]]
		shuffle(view[1])
		shuffle(args)
		return res[0](view[0](view[1][0](args[0]), view[1][1](args[1])), res[1]())

	def step(self):
		return self.unique_terms


class Type(Homogeneous):
	"""Дополнительный класс"""
	def __init__(self):
		self.templates_1 = [
			'(x1 == x2) —> (x2 == x3) == 1',
			'(x1 & y1) == (!x2 | !y2)',
			'(x1 != y1) == (x2 == y2)',
			'!(x1 == x2) & (!x1 == x3) == 0',
			'(x1 == !x2) & (!x1 == x3) == 0',
			'(!(x1 == y1)) == (x2 == y2)',
			'(x1 | y1) -> (x2 & y2) == 0',
			'(x1 & y1) == (!x2 | !y2)',
			'(!(x1 == x2) | !(y1 == y2)) == 1',
			'(!x1 | y1) -> (!x2 & y2) == 1',
			'(x1 -> x2) & (y1 -> y2) == 1',
			'(x1 -> x2) & (x1 -> y1) == 1',
			'!(x1 == x2) & (x1 | x3) & (!x1 | !x3) == 0',
			'(x1 & x2) | (!x1 & !x2) | (x1 == x3) == 1',
			'(x1 & !x2) | (!x1 & x2) | (x2 & x3) | (!x2 & !x3) == 1',
			'(x1 & x2) | (!x1 & !x2) | (x2 & !x3) | (!x2 & x3) == 1',
			'!((!x1 & x2 & !x3) | (!x1 & x2 & x3) | (x1 & !x2 & !x3)) == 1',
			'((x1 == y1) -> (x2 == y2)) & (x1 -> x2) & (y1 -> y2) == 1',
			'(!x1 & x2 & x3) | (x1 & !x2 & x3) | (x1 & x2 & !x3) == 1',
			'((x1 == x2) -> (x2 == x3)) & ((y1 == y2) -> (y2 == y3)) == 1',
		]
		self.templates_2 = [
			'(x1 | x2) -> (x3 | x4) == 1',
			'(x1 -> x2) -> (x3 -> x4) == 1',
			'((x1 == x2) | (x3 == x4)) & (!(x1 == x2) | !(x3 == x4)) == 1',
			'((x1 == x2) & (x3 == x4)) | (!(x1 == x2) & !(x3 == x4)) == 0',
			'(x1 & !x2) | (!x1 & x2) | (x3 & x4) | (!x3 & !x4) == 1',
			'(x1 & x2) | (!x1 & !x2) | (!x3 & x4) | (x3 & !x4) == 1',
		]
		super().__init__()

	def category(self):
		return super().category() + 'Тип 0'


class Type1(Homogeneous):
	def __init__(self):
		main = choice(BinaryLogicOperation.__subclasses__())
		left = choice(BinaryLogicOperation.__subclasses__())
		right = choice(BinaryLogicOperation.__subclasses__())
		equal = choice([Equal, Notequal])
		result = choice(Constant.__subclasses__())
		terms = choice([self.params1, self.params2, self.params3, self.params4])()
		self.template = equal(main(Brackets(left(terms[0], terms[1])), Brackets(right(terms[2], terms[3]))), result())
		super().__init__()

	def category(self):
		return super().category() + 'Тип 1'

	def params1(self):
		x = choice(letters)
		t = [Variable(x + str(k)) for k in range(1, 5)]
		shuffle(t)
		return t

	def params2(self):
		x = choice(letters)
		t = [Variable(x + str(k)) for k in range(1, 5)]
		shuffle(t)
		t += [Variable(x + str(choice([t[0].order, t[1].order])))]
		return t

	def params3(self):
		s = list(range(len(letters)))
		a = s.pop(randint(0, len(s) - 1))
		b = s.pop(randint(0, len(s) - 1))
		x, y = letters[a], letters[b]
		t = [Variable(x + str(k)) for k in range(1, 4)] + [Variable(y + '1')]
		shuffle(t)
		return t

	def params4(self):
		s = list(range(len(letters)))
		a = s.pop(randint(0, len(s) - 1))
		b = s.pop(randint(0, len(s) - 1))
		x, y = letters[a], letters[b]
		t1 = [Variable(x + str(k)) for k in range(1, 3)]
		t2 = [Variable(x + str(randint(1, 2))), Variable(y + '1')]
		shuffle(t1)
		shuffle(t2)
		return t1 + t2

