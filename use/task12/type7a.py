from .common import *
from random import randint

class Type7b(Common):
    def __init__(self):
        self.task = MaskedHostAddressDeterminatedLimitedMask()
        self.number = randint(1, 2 ** (32 - self.task.netmask().ones()) - 2)

    def category(self):
        return Common.category(self) + 'Тип 7a'

    def question_text(self):
        question = "Для узла с IP-адресом {host} адрес сети равен {network}. Определите какой IP-адрес в этой сети будет иметь компьютер с номером по порядку {number}."
        return Common.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'network': self.latex(self.task.network()), 'number': self.number})

    def question_answer(self):
        return self.task.neighbor(self.number)
