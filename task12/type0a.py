from .common import Generator_12, TripleIPAddresses

class Generator_12_type0(Generator_12):
    def __init__(self):
        self.task = TripleIPAddresses()

    def category(self):
        return super(type(self), self).category() + 'Тип 0'

    def question_text(self):
        question = "Определите адрес сети, если адрес компьютера в этой сети {ip}, а маска сети {netmask}. В качестве ответа укажите сумму всех байт адреса сети в виде десятичного числа."
        return Generator_12.question_text(self) + question.format(**{'ip': self.latex(self.task.host()), 'netmask': self.latex(self.task.netmask())})

    def question_answer(self):
        return str(sum(self.task.network()))
