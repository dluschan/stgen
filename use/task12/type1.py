from .common import *
from random import choice


class Type1(Task12):
    def __init__(self):
        self.task = MaskedHostAddressDeterminate()
        self.order = [["первый слева", "четвёртый справа"], ["второй слева", "третий справа"], ["третий слева", "второй справа"], ["четвёртый слева", "первый справа"]]
        self.byte = (self.task.netmask().ones() - 1) // 8

    def category(self):
        return Task12.category(self) + 'Тип 1'

    def question_text(self):
        question = " Для узла с IP-адресом {host} адрес сети равен {network}. Определите чему равен {order} байт маски. Ответ запишите в виде десятичного числа."
        return Task12.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'network': self.latex(self.task.network()), 'order': choice(self.order[self.byte])})

    def question_answer(self):
        return self.task.netmask()[3 - self.byte]
