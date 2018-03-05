from .common import *

class Type3(Common):
    def __init__(self):
        self.task = TripleIPAddresses()

    def category(self):
        return Common.category(self) + 'Тип 3'

    def question_text(self):
        question = "Для узла с IP-адресом {host} адрес сети равен {network}. Определите для скольких различных значений маски это возможно.<br>Ответ запишите в виде десятичного числа."
        return Common.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'network': self.latex(self.task.network())})

    def question_answer(self):
        return len(self.task.suitable())
