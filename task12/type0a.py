from .common import *

class Type0a(Common):
    def __init__(self):
        self.task = TripleIPAddresses()

    def category(self):
        return Common.category(self) + 'Тип 0a'

    def question_text(self):
        question = "Определите адрес сети, если адрес компьютера в этой сети {host}, а маска сети {netmask}. В качестве ответа укажите адрес сети, записанный по тем же правилам, что и IP-адрес."
        return Common.question_text(self) + question.format(**{'host': self.latex(self.task.host()), 'netmask': self.latex(self.task.netmask())})

    def question_answer(self):
        return sum(self.task.network())
