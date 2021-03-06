from .common import *


class Type0b(Task12):
    def __init__(self):
        self.task = MaskedHostAddress()

    def category(self):
        return Task12.category(self) + 'Тип 0b'

    def question_text(self):
        question = "Определите адрес сети, если адрес компьютера в этой сети {host}, а маска сети {netmask}. В качестве ответа укажите адрес сети, записанный по тем же правилам, что и IP-адрес."
        return Task12.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'netmask': self.latex(self.task.netmask())})

    def question_answer(self):
        return self.task.network()
