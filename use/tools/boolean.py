class Term:
	def braced(self, priority):
		return '\\left(' + str(self) + '\\right)' if self.priority < priority else '{' + str(self) + '}'


class Brackets(Term):
	priority = 4

	def __init__(self, *args):
		assert(len(args) == 1)
		self.args = args

	def __str__(self):
		return '(' + str(self.args[0]) + ')'

	def __repr__(self):
		return '\\left(' + repr(self.args[0]) + '\\right)'

	@staticmethod
	def __call__(self, **kwargs):
		return self.args[0](**kwargs)


class Variable(Term):
	priority = 5

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
	priority = 5

	def __init__(self):
		pass


class TrueConst(Constant):
	@staticmethod
	def __repr__():
		return '1'

	@staticmethod
	def __call__(**kwargs):
		return True


class FalseConst(Constant):
	@staticmethod
	def __repr__():
		return '0'

	@staticmethod
	def __call__(**kwargs):
		return False


class LogicOperation(Term):
	pass


class UnaryLogicOperation(LogicOperation):
	priority = 4

	def __init__(self, *args):
		assert(len(args) == 1)
		self.args = args

	def __repr__(self):
		return self.repr + self.args[0].braced(self.priority)

	def __call__(self, **kwargs):
		return self.operation(self.args[0](**kwargs))


class Positive(UnaryLogicOperation):
	repr = ''

	@staticmethod
	def operation(a):
		return a


class Negation(UnaryLogicOperation):
	repr = '\\overline'

	@staticmethod
	def operation(a):
		return not a


class BinaryLogicOperation(LogicOperation):
	priority = 0

	def __init__(self, *args):
		assert(len(args) == 2)
		self.args = args

	def __repr__(self):
		return self.args[0].braced(self.priority) + self.repr + self.args[1].braced(self.priority)

	def __str__(self):
		return self.args[0].braced(self.priority) + self.symbol + self.args[1].braced(self.priority)

	def __call__(self, **kwargs):
		return self.operation(self.args[0](**kwargs), self.args[1](**kwargs))


class Conjunction(BinaryLogicOperation):
	priority = 3
	repr = '\\wedge'

	@staticmethod
	def operation(a, b):
		return a and b


class Disjunction(BinaryLogicOperation):
	priority = 2
	repr = '\\vee'

	@staticmethod
	def operation(a, b):
		return a or b


class Implication(BinaryLogicOperation):
	priority = 1
	repr = '\\implies'

	@staticmethod
	def operation(a, b):
		return not a or b


class Equal(BinaryLogicOperation):
	priority = 0
	repr = '\\equiv'

	@staticmethod
	def operation(a, b):
		return a == b


class Notequal(BinaryLogicOperation):
	priority = 0
	repr = '\\neq'

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

