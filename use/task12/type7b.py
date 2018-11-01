from .common import *
from random import randint


class Type7b(Task12):
    def __init__(self):
        self.task = LimitMaskedHostAddressDeterminate()
        self.number = randint(1, 2 ** (32 - self.task.netmask().ones()) - 2)

    def category(self):
        return Task12.category(self) + 'Тип 7b'

    def question_text(self):
        question = "Для узла с IP-адресом {host} маска сети равна {netmask}. Определите какой IP-адрес в этой сети будет иметь компьютер с номером по порядку {number}."
        return Task12.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'netmask': self.latex(self.task.netmask()), 'number': self.number})

    def question_answer(self):
        return self.task.neighbor(self.number)
