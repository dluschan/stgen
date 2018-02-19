from boolean import *
import itertools, functools, random

unary = [Positive, Negation]
binary = [Conjunction, Disjunction, Implication, Equal, Notequal]

def booltable(n, base = 2):
    '''Функция возвращает таблицу со всеми возможными комбинациями логических переменных в виде списка списков значений'''
    return [[arg // (base ** i) % base for i in range(n)] for arg in range(base**n)]

def truthtable(f, names):
    '''Функция возвращает таблицу истинности логической функции f, столбцы которой задаются в списке names'''
    return [row + [int(f(**dict(zip(map(str, names), row))))] for row in booltable(len(names))]

def check(f, names, limitations):
    '''Функция проверяет последовательность переменных names с каждой строкой из фрагмента таблицы истинности limitations функции f'''
    return all([int(f(**dict(zip(map(str, names), limit[:-1])))) == limit[-1] for limit in limitations])

def singlepicking(mask, truth):
    '''Возвращает те строки из таблицы истинности, которые удовлетворяют маске.
    Значения 2 в маске означают любую переменную, а 1 и 0 - истину и ложь соответственно'''
    return list(filter(lambda line: all([a in [b, 2] for a, b in zip(mask, line)]), truth))

def multipicking(masks, truth):
    '''Возвращает список подходящих под каждую маску из списка масок строк из таблицы истинности.
    Значения 2 в маске означают любую переменную, а 1 и 0 - истину и ложь соответственно'''
    return [singlepicking(mask, truth) for mask in masks]

def filteredmultipicking(masks, truth):
    '''Функция фильтрует все комбинации '''
    return list(*filter(lambda s: len(set((tuple(x) for x in s))) == len(s), itertools.product(*multipicking(masks, truth))))

def output(data):
    '''Функция выводит на экран списко строк таблицы истинности'''
    print(*data, sep = '\n')

def generate_terms(k, alphabet):
    '''Функция отбирает k случайных переменных из переданного ей алфавита alphabet'''
    names = list(alphabet)
    random.shuffle(names)
    return [Term(x) for x in names[:k]]

def create_function(terms):
    '''Функция создаёт случайную логическую функцию от переменных в списке terms'''
    return functools.reduce(lambda x, y: random.choice(binary)(x, y), terms)

def checkdeterminate(f, order, limitations, table):
    '''Функция проверяет единственность порядка переменных order, соответствующего ограничениям limitations из таблицы истинности table функции f'''
    return sum([1 if check(f, order, filteredmultipicking(limitations, table)) else 0 for order in itertools.permutations(terms)]) == 1

def generate_slice_table(f, terms):
    '''Функция возвращает такой срез (подмножество) таблицы истинности логической функции f, по которой можно восстановить порядок переменных в таблице, либо пустой список, если такого среза не существует'''
    table = truthtable(f, terms)
    for k in range(1, len(table) + 1):
        for limitations in itertools.combinations(table, k):
            if checkdeterminate(f, order, limitations, table):
                return list(limitations)
    else:
        return []

if __name__ == "__main__":
    pass
