from .. import notation, generator
from random import randint, choice, shuffle
import json, sys, hmac, hashlib

class Generator_01(generator.BaseGenerator):
    '''Задача номер 1'''
    def category(self):
        return '$course$/ЕГЭ/Задача 1/'

    def question_type(self):
        return 'shortanswer'

    def cdata(self):
        return False

view = [0, 1, 2, 3, 4, 5, 6]

digits = '0123456789abcdefghijklmnopqrstuvwxyz'
bases = {2: 'двоичная', 3: 'троичная', 4: 'четверичная', 5: 'пятиричная', 6: 'шестиричная', 7: 'семиричная', 8: 'восьмиричная', 9: 'девятиричная', 11: 'одиннадцатиричная', 12: 'двенадцатиричная', 13: 'тринадцатиричная', 14: 'четырнадцатиричная', 15: 'пятнадцатиричная', 16: 'шестнадцатиричная'}
intro = 'В системе счисления с основанием n < 37 используются первые n цифр из списка {digits} по порядку.'
quetions = [
    'Определите сколько цифр {digit} содержит {base} запись числа {number}.',
    'Определите сколько различных цифр содержит {base} запись числа {number}.',
    'Определите сколько значащих цифр содержит {base} запись числа {number}.',
    'Определите наименьшую значащую цифру, которую содержит {base} запись числа {number}.',
    'Определите наибольшую значащую цифру, которую содержит {base} запись числа {number}.',
    'Определите наименьшее содержащее {m} цифр число в системе счисления {bigbase}, запись которого в системе счисления {base} содержит ровно {k} цифр {digit}.',
    'Определите наибольшее содержащее {m} цифр число в системе счисления {bigbase}, запись которого в системе счисления {base} содержит ровно {k} цифр {digit}.'
]

def s5(m, p, base, k, digit):
    '''Решение задачи типа 5'''
    rest = (m - 1) * p - k
    assert(rest >= -1)
    return notation.transform('1' if rest > -1 else '' + '0' * ((m - 1) * p - k) + str(digit) * k, base**p, digits)

def s6(m, p, base, k, digit):
    '''Решение задачи типа 6'''
    return notation.transform('1' + '0' * ((m - 1) * p - k) + str(digit) * k, base**p, digits)

class BaseQuestion:
    def category():
        return "$course$/ЕГЭ/Задача 1/Тип 6"

    def question_type():
        return "$course$/ЕГЭ/Задача 1/Тип 6"

def generate():
    r = {"category": "$course$/ЕГЭ/Задача 1/Тип 6", "question_type": "shortanswer", "questions": []}
    for i in range(10 if len(sys.argv) == 1 else int(sys.argv[1])):
        task, answer = type6.generate()
        r["questions"].append({"question_name": "Задача №" + hmac.new(bytearray(task,'utf-8'), bytearray('text','utf-8'), hashlib.sha1).hexdigest(), "question_text": task, "question_answer": answer})
    return json.dumps(r)

if __name__ == "__main__":
    print(generate())
