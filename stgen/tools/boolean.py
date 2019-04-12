"""Реализация логических констант, переменных, унарных и бинарных операций, скобок в логических выражениях."""


class Term:
	"""Базовый класс для всех термов логического выражения."""
	pass


class Membership(Term):
	"""Принадлежность переменной множеству."""
	priority = 7

	def __init__(self, element, container):
		self.element = element
		self.container = container

	def __repr__(self):
		return '(' + self.element + ' \\in ' + self.container + ')'

	def __str__(self):
		return '(' + self.element + ' ∈ ' + self.container + ')'

	def __call__(self, **kwargs):
		return kwargs[str(self)]

	def __hash__(self):
		return hash(str(self))

	def __eq__(self, other):
		return self.element == other.element and self.container == other.container


class NotMembership(Term):
	"""Не принадлежность переменной множеству."""
	priority = 7

	def __init__(self, element, container):
		self.element = element
		self.container = container

	def __repr__(self):
		return '(' + self.element + ' \\notin ' + self.container + ')'

	def __str__(self):
		return '(' + self.element + ' ∉ ' + self.container + ')'

	def __call__(self, **kwargs):
		return kwargs[str(self)]

	def __hash__(self):
		return hash(str(self))

	def __eq__(self, other):
		return self.element == other.element and self.container == other.container


class Variable(Term):
	"""Логическая переменная."""
	priority = 7

	def __init__(self, name):
		assert(type(name) == str)
		self.family = name[0]
		self.order = int(name[1:])

	def __repr__(self):
		return self.family + '_{' + str(self.order) + '}'

	def __str__(self):
		return self.family + str(self.order)

	def __call__(self, **kwargs):
		return kwargs[str(self)]

	def __hash__(self):
		return hash(str(self))

	def __eq__(self, other):
		return self.family == other.family and self.order == other.order


class Constant(Term):
	"""Логическая константа."""
	priority = 7


class TrueConst(Constant):
	"""Логическая истина."""
	@staticmethod
	def __repr__():
		return '1'

	@staticmethod
	def __call__(**kwargs):
		return True


class FalseConst(Constant):
	"""Логическая ложь."""
	@staticmethod
	def __repr__():
		return '0'

	@staticmethod
	def __call__(**kwargs):
		return False


class LogicOperation(Term):
	"""Базовый класс для логических операций."""
	def __eq__(self, other):
		return type(self) == type(other) and self.args == other.args


class UnaryLogicOperation(LogicOperation):
	"""Базовый класс для унарных логических операций и скобок."""
	def __init__(self, *args):
		assert(len(args) == 1)
		self.args = args

	def __repr__(self):
		return self.repr + ' ' + repr(self.args[0])

	def __str__(self):
		return self.symbol + ' ' + str(self.args[0])

	def __call__(self, **kwargs):
		return self.operation(self.args[0](**kwargs))


class Positive(UnaryLogicOperation):
	"""Тривиальная обёртка над логическим термом."""
	priority = 5
	repr = ''
	symbol = ''

	@staticmethod
	def operation(a):
		return a


class Negation(UnaryLogicOperation):
	"""Отрицание."""
	priority = 5
	repr = '\\overline'
	symbol = '!'

	@staticmethod
	def operation(a):
		return not a


class Brackets(UnaryLogicOperation):
	"""Скобки, используются для повышения приоритета логической операции."""
	priority = 6

	@staticmethod
	def operation(a):
		return a

	def __repr__(self):
		return '\\left(' + ' ' + repr(self.args[0]) + ' ' + '\\right)'

	def __str__(self):
		return '(' + str(self.args[0]) + ')'


class BinaryLogicOperation(LogicOperation):
	"""Базовый класс для бинарных логических операций."""
	def __init__(self, *args):
		assert(len(args) == 2)
		self.args = args

	def __repr__(self):
		return repr(self.args[0]) + ' ' + self.repr + ' ' + repr(self.args[1])

	def __str__(self):
		return str(self.args[0]) + ' ' + self.symbol + ' ' + str(self.args[1])

	def __call__(self, **kwargs):
		return self.operation(self.args[0](**kwargs), self.args[1](**kwargs))


class Conjunction(BinaryLogicOperation):
	"""Коньюнкция."""
	priority = 4
	repr = '\\wedge'
	symbol = '&'

	@staticmethod
	def operation(a, b):
		return a and b


class Disjunction(BinaryLogicOperation):
	"""Дизьюнкция."""
	priority = 3
	repr = '\\vee'
	symbol = '|'

	@staticmethod
	def operation(a, b):
		return a or b


class Implication(BinaryLogicOperation):
	"""Импликация."""
	priority = 2
	repr = '\\implies'
	symbol = '->'

	@staticmethod
	def operation(a, b):
		return not a or b


class Equal(BinaryLogicOperation):
	"""Равенство."""
	priority = 1
	repr = '\\equiv'
	symbol = '=='

	@staticmethod
	def operation(a, b):
		return a == b


class NotEqual(BinaryLogicOperation):
	"""Неравенство."""
	priority = 1
	repr = '\\neq'
	symbol = '!='

	@staticmethod
	def operation(a, b):
		return a != b


def analyze(t):
	r = {}
	ranalyze(t, r)
	return r


def ranalyze(t, r):
	if type(t) in [FalseConst, TrueConst]:
		pass
	elif type(t) == Variable:
		if t.family not in r:
			r[t.family] = [t.order]
		elif t.order not in r[t.family]:
			r[t.family] += [t.order]
	elif type(t) in UnaryLogicOperation.__subclasses__() + BinaryLogicOperation.__subclasses__():
		for arg in t.args:
			ranalyze(arg, r)


def shift(t, k):
	import copy
	c = copy.deepcopy(t)
	rshift(c, k)
	return c


def rshift(t, k):
	if type(t) in [FalseConst, TrueConst]:
		pass
	elif type(t) == Variable:
		t.order += k if type(k) == int else k[t.family]
	elif type(t) in UnaryLogicOperation.__subclasses__() + BinaryLogicOperation.__subclasses__():
		for arg in t.args:
			rshift(arg, k)


def terms(t):
	r = []
	rterms(t, r)
	return r


def rterms(t, r):
	if type(t) in [FalseConst, TrueConst]:
		pass
	elif type(t) == Variable and t not in r:
		r.append(t)
	elif type(t) in UnaryLogicOperation.__subclasses__() + BinaryLogicOperation.__subclasses__():
		for arg in t.args:
			rterms(arg, r)


def varlist(t):
	z = analyze(t)
	return [key + str(order) for key in z for order in z[key]]


def simplify_not_equality(term):
	"""simplify not equality:

	replace "x != y" with "(!x & y) | (x & !y)"
	"""
	if type(term) == NotEqual:
		return Disjunction(
			Conjunction(Negation(simplify_not_equality(term.args[0])), simplify_not_equality(term.args[1])),
			Conjunction(simplify_not_equality(term.args[0]), Negation(simplify_not_equality(term.args[1]))),
		)
	elif isinstance(term, LogicOperation):
		return type(term)(*map(simplify_not_equality, term.args))
	else:
		return term


def simplify_equality(term):
	"""simplify equality:

	replace "x == y" with "(!x | y) & (x | !y)"
	"""
	if type(term) == Equal:
		return Conjunction(
			Disjunction(Negation(simplify_equality(term.args[0])), simplify_equality(term.args[1])),
			Disjunction(simplify_equality(term.args[0]), Negation(simplify_equality(term.args[1]))),
		)
	elif isinstance(term, LogicOperation):
		return type(term)(*map(simplify_equality, term.args))
	else:
		return term


def simplify_implication(term):
	"""simplify implication:

	replace "x -> y" with "!x | y"
	"""
	if type(term) == Implication:
		return Disjunction(Negation(simplify_implication(term.args[0])), simplify_implication(term.args[1]))
	elif isinstance(term, LogicOperation):
		return type(term)(*map(simplify_implication, term.args))
	else:
		return term


def simplify_negation(term):
	"""simplify negation:

	replace "!!x" with "x"
	replace "!(x | y)" with "!x & !y"
	replace "!(x & y)" with "!x | !y"
	replace "!(x ∈ A)" with "x ∉ A"
	replace "!(x ∉ y)" with "x ∈ A"
	"""
	if type(term) == Negation and type(term.args[0]) == Negation:
		return simplify_negation(term.args[0].args[0])
	elif type(term) == Negation and type(term.args[0]) == Conjunction:
		return Disjunction(
			simplify_negation(Negation(term.args[0].args[0])),
			simplify_negation(Negation(term.args[0].args[1]))
		)
	elif type(term) == Negation and type(term.args[0]) == Disjunction:
		return Conjunction(
			simplify_negation(Negation(term.args[0].args[0])),
			simplify_negation(Negation(term.args[0].args[1]))
		)
	elif type(term) == Negation and type(term.args[0]) == Membership:
		return NotMembership(term.args[0].element, term.args[0].container)
	elif type(term) == Negation and type(term.args[0]) == NotMembership:
		return Membership(term.args[0].element, term.args[0].container)
	elif isinstance(term, LogicOperation):
		return type(term)(*map(simplify_negation, term.args))
	else:
		return term


def simplify_disjunction_of_conjunction(term):
	"""
	simplify disjunction of conjunction

	replace "(x & y) | z" with "(x | z) & (y | z)"
	replace "x | (y & z)" with "(x | y) & (x | z)"
	"""
	if type(term) == Disjunction and type(term.args[0]) == Conjunction:
		return Conjunction(
			Disjunction(
				simplify_disjunction_of_conjunction(term.args[0].args[0]),
				simplify_disjunction_of_conjunction(term.args[1])
			),
			Disjunction(
				simplify_disjunction_of_conjunction(term.args[0].args[1]),
				simplify_disjunction_of_conjunction(term.args[1])
			)
		)
	elif type(term) == Disjunction and type(term.args[1]) == Conjunction:
		return Conjunction(
			Disjunction(
				simplify_disjunction_of_conjunction(term.args[0]),
				simplify_disjunction_of_conjunction(term.args[1].args[0])
			),
			Disjunction(
				simplify_disjunction_of_conjunction(term.args[0]),
				simplify_disjunction_of_conjunction(term.args[1].args[1])
			)
		)
	elif isinstance(term, LogicOperation):
		return type(term)(*map(simplify_disjunction_of_conjunction, term.args))
	else:
		return term


def simplify_conjunction_of_disjunction(term):
	"""
	simplify conjunction of disjunction

	replace "(x | y) & z" with "(x & z) | (y & z)"
	replace "x & (y | z)" with "(x & y) | (x & z)"
	"""
	if type(term) == Conjunction and type(term.args[0]) == Disjunction:
		return Disjunction(
			Conjunction(
				simplify_conjunction_of_disjunction(term.args[0].args[0]),
				simplify_conjunction_of_disjunction(term.args[1])
			),
			Conjunction(
				simplify_conjunction_of_disjunction(term.args[0].args[1]),
				simplify_conjunction_of_disjunction(term.args[1])
			)
		)
	elif type(term) == Conjunction and type(term.args[1]) == Disjunction:
		return Disjunction(
			Conjunction(
				simplify_conjunction_of_disjunction(term.args[0]),
				simplify_conjunction_of_disjunction(term.args[1].args[0])
			),
			Conjunction(
				simplify_conjunction_of_disjunction(term.args[0]),
				simplify_conjunction_of_disjunction(term.args[1].args[1])
			)
		)
	elif isinstance(term, LogicOperation):
		return type(term)(*map(simplify_conjunction_of_disjunction, term.args))
	else:
		return term


def multi_simplify_disjunction_of_conjunction(term):
	"""apply many times simplify_conjunction_of_disjunction"""
	while simplify_disjunction_of_conjunction(term) != term:
		term = simplify_disjunction_of_conjunction(term)
	return term


def multi_simplify_conjunction_of_disjunction(term):
	"""apply many times simplify_conjunction_of_disjunction"""
	while simplify_conjunction_of_disjunction(term) != term:
		term = simplify_conjunction_of_disjunction(term)
	return term


def unbrackets(term):
	"""remove brackets from term"""
	if type(term) == Brackets:
		return unbrackets(term.args[0])
	elif isinstance(term, LogicOperation):
		return type(term)(*map(unbrackets, term.args))
	else:
		return term


def brackets(term):
	"""place brackets into term"""
	if isinstance(term, LogicOperation):
		return type(term)(*map(lambda t: Brackets(brackets(t)) if t.priority < term.priority else brackets(t), term.args))
	else:
		return term


def get_disjunctions_from_conjuction(term):
	"""get list disjunctions from term. term - conjunctive normal form expression"""
	if type(term) == Conjunction:
		return get_disjunctions_from_conjuction(term.args[0]) + get_disjunctions_from_conjuction(term.args[1])
	elif type(term) == Brackets:
		return [term.args[0]]
	elif type(term) == Disjunction:
		return [term]
	else:
		return [term]


def get_primary_terms_from_disjunctios(term):
	"""get list term from term. term - disjunctios normal form expression"""
	if type(term) == Disjunction:
		return get_primary_terms_from_disjunctios(term.args[0]) + get_primary_terms_from_disjunctios(term.args[1])
	else:
		return [term]


def cnf(term):
	"""conjunctive normal form"""
	return brackets(multi_simplify_disjunction_of_conjunction(simplify_negation(
		simplify_implication(simplify_equality(simplify_not_equality(unbrackets(term))))))
	)
