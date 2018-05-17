from .common import *

class Type6b(Common):
    def __init__(self):
        self.task = MaskedHostAddressDeterminatedLimitedMask()

    def category(self):
        return Common.category(self) + 'Тип 6b'

    def question_text(self):
        question = "Для узла с IP-адресом {host} маска сети равна {netmask}. Определите какой номер по порядку имеет данный компьютер в сети.<br>Ответ запишите в виде десятичного числа."
        return Common.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'netmask': self.latex(self.task.netmask())})

    def question_answer(self):
        return self.task.hostnumber()
