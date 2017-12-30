from random import randint, choice, shuffle
import subprocess, json, sys, hmac, hashlib

def task(n, k, m):
    'Функция генерирует текст вопроса'
    digit = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
    base = {2: 'двоичная', 3: 'троичная', 4: 'четверичная', 5: 'пятиричная', 6: 'шестиричная', 7: 'семиричная', 8: 'восьмиричная', 9: 'девятиричная', 11: 'одиннадцатиричная', 12: 'двенадцатиричная', 13: 'тринадцатиричная', 14: 'четырнадцатиричная', 15: 'пятнадцатиричная', 16: 'шестнадцатиричная'}
    return 'Определите сколько цифр ' + digit[m] + ' содержит ' + base[k] + ' запись числа ' + str(n) + '.'

def solve(n, k, m):
    'Функция подсчитывает количество путей в графе'
    count = 0
    while n:
        if n % k == m:
            count += 1
        n //= k
    return count

def generate():
    r = {"category": "ЕГЭ по информатике задача 1", "question_type": "numerical", "questions": []}
    for i in range(10 if len(sys.argv) == 1 else int(sys.argv[1])):
        n = randint(10, 10**5)
        k = choice([2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16])
        m = randint(0, k - 1)
        r["questions"].append({"question_name": "Задача №" + hmac.new(bytearray(task(n, k, m),'utf-8'), bytearray('text','utf-8'), hashlib.sha1).hexdigest(), "question_text": task(n, k, m), "question_answer": solve(n, k, m)})
    return json.dumps(r)

print(generate())
