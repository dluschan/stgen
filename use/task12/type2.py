from .common import *

class Type2(Common):
    def __init__(self):
        self.task = MaskedHostAddressDeterminatedLimitedMask()

    def category(self):
        return Common.category(self) + 'Тип 2'

    def question_text(self):
        question = "Для узла с IP-адресом {host} адрес сети равен {network}. Определите сколько компьютеров может быть в этой сети, если два служебные адреса: широковещательный и адрес сети — не используются компьютерами.<br>Ответ запишите в виде десятичного числа."
        return Common.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'network': self.latex(self.task.network())})

    def question_answer(self):
        return 2**(32 - self.task.netmask().ones()) - 2
