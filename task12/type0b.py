from .common import Common, TripleIPAddresses

class Type0b(Common):
    def __init__(self):
        self.task = TripleIPAddresses()

    def category(self):
        return super(type(self), self).category() + 'Тип 0b'

    def question_text(self):
        question = "Определите адрес сети, если адрес компьютера в этой сети {ip}, а маска сети {netmask}. В качестве ответа укажите адрес сети в виде 4 байт разделённых точками."
        return Generator_12.question_text(self) + question.format(**{'ip': self.latex(self.task.host()), 'netmask': self.latex(self.task.netmask())})

    def question_answer(self):
        return str(sum(self.task.network()))
