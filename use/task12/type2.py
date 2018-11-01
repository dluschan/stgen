from .common import *


class Type2(Task12):
    def __init__(self):
        self.task = LimitMaskedHostAddressDeterminate()

    def category(self):
        return Task12.category(self) + 'Тип 2'

    def question_text(self):
        question = "Для узла с IP-адресом {host} адрес сети равен {network}. Определите сколько компьютеров может быть в этой сети, если два служебные адреса: широковещательный и адрес сети — не используются компьютерами.<br>Ответ запишите в виде десятичного числа."
        return Task12.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'network': self.latex(self.task.network())})

    def question_answer(self):
        return 2**(32 - self.task.netmask().ones()) - 2
