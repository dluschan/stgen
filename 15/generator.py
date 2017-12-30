from random import randint, choice, shuffle
import subprocess, json, sys, hmac, hashlib

def horizontal(x):
    'Функция устанавливает горизонтальные (т.е. между вершинами одного слоя) связи в графе'
    k = randint(1, (len(x) + 1) // 2)
    hor = set()
    while len(hor) < k:
        hor.add(choice(x[:-1]))
    res = []
    for w in hor:
        res.append((w, w+1))
    return res

def distribution(a, b):
    'Функция разбивает список a на b промежутков'
    e = list(range(2, len(a) - 1))
    assert(len(e) >= b - 1)
    shuffle(e)
    s = sorted(e[:b - 1] + [0] + [len(a)])
    r = []
    for i in range(b):
        r.append(a[s[i]: s[i+1]])
    return r

def addition(x, y):
    'Функция получает два списка и расширяет меньший из них с помощью дубликатов его элементов, чтобы списки сравнялись по длине'
    if len(x) < len(y):
        a, b = x, y
        r = False
    else:
        a, b = y, x
        r = True
    c = []
    while len(a) + len(c) < len(b):
        c.append(choice(a))
    a += c
    a.sort()
    if r:
        a, b = b, a
    return list(zip(a, b))

def graph(n):
    'Функция генерирует граф заданной длины из набора вершин в виде списка пар вершин'
    k = randint(3, (n + 2) // 3)
    levels = [[0], *distribution(list(range(1, n - 1)), k), [n - 1]]
    res = []
    for i in range(len(levels) - 1):
        if len(levels[i]) >= 2:
            res += horizontal(levels[i][:])
        res += addition(levels[i][:], levels[i+1][:])
    return res

def dot_graph(g, s):
    'Конвертирует граф в формат dot с переименованием вершин согласно строке s'
    res = 'digraph G {node [shape = circle];rankdir = LR;'
    for link in g:
        res += s[link[0]] + '->' + s[link[1]] + ';'
    res += '}'
    return res

def task(n, s):
    'Функция генерирует текст вопроса'
    return 'На рисунке - схема дорог, связывающих города ' + ', '.join(s[:n]) + '. По каждой дороге можно двигаться только в одном направлении, указанном стрелкой. Сколько существует различных путей из города ' + s[0] + ' в город ' + s[n-1] + '?'

def dict_graph(links):
    'Функция преобразовывает граф из списка связей в список списков'
    res = {}
    for key in set([x[0] for x in links] + [x[1] for x in links]):
        res[key] = [y[0] for y in filter(lambda x: x[1] == key, links)]
    return res

def solve(links, start, end):
    'Функция подсчитывает количество путей в графе'
    if start == end:
        return 1
    else:
        return sum([solve(links, start, finish) for finish in links[end]])

def dot(g, s):
    return subprocess.Popen("echo \"" + dot_graph(g, s) + "\" | dot -Tsvg | base64", shell = True, stdout = subprocess.PIPE).stdout.read().decode('utf-8')

def generate():
    s = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    r = {"category": "ЕГЭ по информатике задача 15", "question_type": "numerical", "questions": []}
    for i in range(10 if len(sys.argv) == 1 else int(sys.argv[1])):
        n = randint(10, 18)
        g = graph(n)
        r["questions"].append({"question_name": "Задача №" + hmac.new(bytearray(dot_graph(g, s),'utf-8'), bytearray('text','utf-8'), hashlib.sha1).hexdigest(), "question_text": task(n, s), "question_media": dot(g, s), "question_answer": solve(dict_graph(g), 0, n - 1)})
    return json.dumps(r)

print(generate())
