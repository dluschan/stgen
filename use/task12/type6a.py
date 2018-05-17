from .common import *

class Type6a(Common):
    def __init__(self):
        self.task = MaskedHostAddressDeterminatedLimitedMask()

    def category(self):
        return Common.category(self) + 'Тип 6a'

    def question_text(self):
        question = "Для узла с IP-адресом {host} адрес сети равен {network}. Определите какой номер по порядку имеет данный компьютер в сети.<br>Ответ запишите в виде десятичного числа."
        return Common.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'network': self.latex(self.task.network())})

    def question_answer(self):
        return self.task.hostnumber()
