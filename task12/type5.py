from .common import *
from random import choice

class Type5(Common):
    def __init__(self):
        self.task = TripleIPAddresses()
        self.extreme = {max: ["наибольшее количество единиц", "наименьшее количество нулей"], min: ["наибольшее количество нулей", "наименьшее количество единиц"]}
        self.key = choice(list(self.extreme.keys()))

    def category(self):
        return Common.category(self) + 'Тип 5'

    def question_text(self):
        question = "Для узла с IP-адресом {host} адрес сети равен {network}. Определите какое {digits} может быть в маске сети.<br>Ответ запишите в виде десятичного числа."
        return Common.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'network': self.latex(self.task.network()), 'digits': choice(self.extreme[self.key])})

    def question_answer(self):
        return self.key(self.task.suitable()).ones()
