from .common import *


class Type3(Task12):
    def __init__(self):
        self.task = MaskedHostAddress()

    def category(self):
        return Task12.category(self) + 'Тип 3'

    def question_text(self):
        question = "Для узла с IP-адресом {host} адрес сети равен {network}. Определите для скольких различных значений маски это возможно.<br>Ответ запишите в виде десятичного числа."
        return Task12.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'network': self.latex(self.task.network())})

    def question_answer(self):
        return len(self.task.suitable())
