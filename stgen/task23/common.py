from ..tools.task import BaseTask
from ..tools.systemeq import *
from ..tools.common import letters
from ..tools.decompose import single_decompose
from random import randint, choice, shuffle


class Task23(BaseTask):
	"""ЕГЭ по информатике - Задача номер 23"""
	def __init__(self):
		super().__init__()
		self.question = '''Определите сколько существует различных наборов значений логических переменных {variables}, 
		которые удовлетворяют системе уравнений {equations}.'''

	def category(self):
		return super().category() + 'Задача 23/'

	def question_text(self):
		return self.question.format(variables=self.latex(''.join(sorted(map(str, self.system.terms)))), equations=self.system)

	def question_answer(self):
		return self.system.count()

	def question_type(self):
		return 'numerical'


class Homogeneous(Task23):
	"""Система однородных уравнений"""
	def __init__(self):
		super().__init__()
		s = self.step()
		self.system = SystemEquation([shift(self.template, dict(zip(s.keys(), map(lambda x: k*x, s.values())))) for k in range(self.eqcount())])

	def eqcount(self):
		n = randint(9, 10)
		return (n - len(terms(self.template))) // max(self.step().values()) + 1

	def step(self):
		return randint(1, len(min(analyze(self.template).values(), key=len)))


def random_unary(term):
	"""Случайная унарная функция."""
	return choice(UnaryLogicOperation.__subclasses__())(term)


def random_binary(terms):
	"""Случайная бинарная логическая функция."""
	assert(len(terms) == 2)
	return choice(BinaryLogicOperation.__subclasses__())(random_unary(terms[0]), random_unary(terms[1]))


def random_function(terms):
	"""Случайная логическая функция, использующая terms как параметры."""
	if len(terms) == 1:
		return random_unary(terms[0])
	if randint(0, 1) == 0:
		return random_function([random_binary(terms[:2])] + terms[2:])
	else:
		return random_binary([terms[0], random_function(terms[1:])])


def random_family(n):
	"""Возвращает список из n различных букв латинского алфавита."""
	s = list(range(len(letters)))
	return [letters[s.pop(randint(0, len(s) - 1))] for _ in range(n)]


def random_unique_terms(family, n):
	"""Возвращает ассоциативный массив с идентификаторами-буквами и количеством букв.

	{'a': 3, 'b': 2}"""
	repeats = single_decompose(n, len(family), n)
	return dict(zip(family, repeats))


def random_extended_terms(unique_terms, n):
	"""Возвращает словарь термов, расширенный с помощью повторов номер до n термов.

	С идентификатором-буквой ассоциирован список из количества уникальных номеров данного семейства термов и
	полного списка номер термов.
	{'a': [3, [2, 1, 3, 2]], 'b': [2, [2, 1, 2]]}"""
	r = {key: [unique_terms[key], list(range(1, unique_terms[key] + 1))] for key in unique_terms}
	for _ in range(n - sum(unique_terms.values())):
		key = choice(list(r.keys()))
		r[key][1].append(randint(1, unique_terms[key]))
	for key in r:
		shuffle(r[key][1])
	return r


def shift_extended_terms(extended_terms, k):
	"""Выполняет k «сдвигов» номеров термов на минимальные непересекающиеся отрезки внутри одного семейстав.

	Например, при k = 1 функция выполнит следующий сдвиг:
	{'a': [3, [2, 1, 3, 2]], 'b': [2, [2, 1, 2]]} -> {'a': [3, [5, 4, 6, 5]], 'b': [2, [4, 3, 4]]}"""
	return {key: [extended_terms[key][0], [value + extended_terms[key][0] * k for value in extended_terms[key][1]]] for key in extended_terms}


def compile_terms(extended_terms):
	"""Компилирует список термов из зашифрованного словаря.

	Пример:
	{'a': [3, [5, 4, 6, 5]], 'b': [2, [4, 3, 4]]} -> ['a5', 'a4', 'a6', 'a5', 'b4', 'b3', 'b4']"""
	r = []
	for key in extended_terms:
		r += [Variable(key + str(order)) for order in extended_terms[key][1]]
	return r

