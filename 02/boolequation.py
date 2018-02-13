import itertools, functools, random

class Term:
    def __init__(self, name):
        assert(type(name) == str)
        self.name = name

    def __str__(self):
        return self.name

    def __call__(self, **kwargs):
        return kwargs[self.name]

class UnaryOperation:
    repr = 'unary'

    operation = lambda self, a: 0

    def __init__(self, *args):
        assert(len(args) == 1)
        self.args = args

    def __str__(self):
        return self.repr + ' { ' + str(self.args[0]) + ' }'

    def __call__(self, **kwargs):
        return self.operation(self.args[0](**kwargs))

Positive = type('Positive', (UnaryOperation,), {'repr': '', 'operation': lambda self, a: a})
Negation = type('Negation', (UnaryOperation,), {'repr': '\\overline', 'operation': lambda self, a: not a})

class BinaryOperation:
    repr = 'binary'

    operation = lambda self, a, b: 0

    def __init__(self, *args):
        assert(len(args) == 2)
        self.args = args

    def __str__(self):
        return '{ ' + str(self.args[0]) + ' } ' + self.repr + ' { ' + str(self.args[1]) + ' }'

    def __call__(self, **kwargs):
        return self.operation(self.args[0](**kwargs), self.args[1](**kwargs))

Conjunction = type('Conjunction', (BinaryOperation,), {'repr': '\\wedge', 'operation': lambda self, a, b: a and b})
Disjunction = type('Disjunction', (BinaryOperation,), {'repr': '\\vee', 'operation': lambda self, a, b: a or b})
Implication = type('Implication', (BinaryOperation,), {'repr': '\\implies', 'operation': lambda self, a, b: not a or b})
Equal = type('Equal', (BinaryOperation,), {'repr': '\\equiv', 'operation': lambda self, a, b: a == b})
Notequal = type('Notequal', (BinaryOperation,), {'repr': '\\neq', 'operation': lambda self, a, b: a != b})

unary = [Positive, Negation]
binary = [Conjunction, Disjunction, Implication, Equal, Notequal]

k = random.randint(2, 5)
names = ['x' + str(i) for i in range(1, k + 1)]
terms = [Term(name) for name in names]
values = [random.randint(0, 1) for i in range(1, k + 1)]
args = dict(zip(names, values))

f = functools.reduce(random.choice(binary), terms)

print(f)
print(args)
print(f(**args))
