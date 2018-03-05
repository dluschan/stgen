from .common import *
from random import randint

class Type7b(Common):
    def __init__(self):
        self.task = TripleIPAddressesDeterminatedLimitedMask()
        self.number = randint(1, 2 ** (32 - self.task.netmask().ones()) - 2)

    def category(self):
        return Common.category(self) + 'Тип 7b'

    def question_text(self):
        question = "Для узла с IP-адресом {host} маска сети равна {netmask}. Определите какой IP-адрес в этой сети будет иметь компьютер с номером по порядку {number}."
        return Common.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'netmask': self.latex(self.task.netmask()), 'number': self.number})

    def question_answer(self):
        return self.task.neighbor(self.number)
