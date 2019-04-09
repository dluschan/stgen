from .boolean import *
from ..tools.common import letters
from ..tools.decompose import single_decompose
from random import randint, choice, shuffle
import itertools, functools, copy

unary = [Positive, Negation]
binary = [Conjunction, Disjunction, Implication, Equal, NotEqual]


def booltable(n, base = 2):
	"""Возвращает таблицу со всеми возможными комбинациями логических переменных в виде списка списков значений"""
	return [[arg // (base ** i) % base for i in range(n)] for arg in range(base**n)]


def truthtable(f, names):
	"""Функция возвращает таблицу истинности логической функции f, столбцы которой задаются в списке names"""
	return [row + [int(f(**dict(zip(map(str, names), row))))] for row in booltable(len(names))]


def count(f, names):
	"""Функция возвращает количество решений логической функции f, от логических переменных names"""
	return sum([1 for row in booltable(len(names)) if f(**dict(zip(map(str, names), row)))])


def check(f, names, limitations):
	"""Проверяет переменные names с каждой строкой из фрагмента таблицы истинности limitations функции f"""
	return all([int(f(**dict(zip(map(str, names), limit[:-1])))) == limit[-1] for limit in limitations])


def singlepicking(mask, truth):
	"""Возвращает те строки из таблицы истинности, которые удовлетворяют маске.

	Значения 2 в маске означают любую переменную, а 1 и 0 - истину и ложь соответственно"""
	return list(filter(lambda line: all([a in [b, 2] for a, b in zip(mask, line)]), truth))


def multipicking(masks, truth):
	"""Возвращает список подходящих под каждую маску из списка масок строк из таблицы истинности.

	Значения 2 в маске означают любую переменную, а 1 и 0 - истину и ложь соответственно"""
	return [singlepicking(mask, truth) for mask in masks]


def filteredmultipicking(masks, truth):
	"""Функция фильтрует все комбинации """
	res = []
	for comb in itertools.product(*multipicking(masks, truth)):
		if len(comb) == len(set([tuple(x) for x in comb])):
			res += list(comb)
	return res


def output(data):
	"""Функция выводит на экран списко строк таблицы истинности"""
	print(*data, sep = "\n")


def create_terms(k, alphabet):
	"""Функция отбирает k случайных переменных из переданного ей алфавита alphabet"""
	names = list(alphabet)
	random.shuffle(names)
	return [Variable(x) for x in names[:k]]


def create_function(terms):
	"""Функция создаёт случайную логическую функцию от переменных в списке terms"""
	#x /\ y \/ (y ≡ z) \/ w
	assert(len(terms) > 3)
	return Disjunction(Disjunction(Conjunction(terms[0], terms[1]), Equal(terms[1], terms[2])), terms[3])


def checkdeterminate(f, terms, limitations, table):
	"""Функция проверяет единственность порядка переменных order, соответствующего ограничениям limitations
	из таблицы истинности table функции f"""
	return sum([1 if check(f, order, filteredmultipicking(limitations, table)) else 0 for order in itertools.permutations(terms)]) == 1


def relieve(limitations):
	"""Функция вставляет в таблицу истинности несколько «2», означающих любое значение переменной"""
	# Не работает
	for i in range(2):
		limitations[random.randint(0, len(limitations) - 1)][random.randint(0, len(limitations[0][:-1]) - 1)] = 2
	return limitations


def generate_slice_table(f, terms):
	"""Функция возвращает такой срез (подмножество) таблицы истинности логической функции f,
	по которому можно восстановить порядок переменных в таблице, либо пустой список,
	если такого среза не существует"""
	table = truthtable(f, terms)
	if not checkdeterminate(f, terms, table, table):
		return [[]]
	for k in range(1, len(table) + 1):
		for limitations in itertools.combinations(table, k):
			lite_limitations = relieve(copy.deepcopy(limitations))
			if checkdeterminate(f, terms, lite_limitations, table):
				return lite_limitations
	return [[]]


def random_unary(term):
	"""Случайная унарная функция."""
	return term if randint(0, 1) == 0 else Negation(term)


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

