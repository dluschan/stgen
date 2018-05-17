from ..generator import BaseGenerator
from ..ip import MaskedHostAddress, MaskedHostAddressDeterminated, MaskedHostAddressDeterminatedLimitedMask

class Common(BaseGenerator):
    '''Задача номер 12'''
    def category(self):
        return '$course$/ЕГЭ/Задача 12/'

    def question_text(self):
        sample = MaskedHostAddress()
        return '''В терминологии сетей TCP/IP маской сети называется двоичное число, определяющее, какая часть IP-адреса узла сети относится к адресу сети, а какая — к адресу самого узла в этой сети. При этом в маске сначала (в старших разрядах) стоят единицы, а затем с некоторого места — нули. Обычно маска записывается по тем же правилам, что и IP-адрес — в виде четырёх байтов, разделённых точками, причём каждый байт записывается в виде десятичного числа. Адрес сети получается в результате применения поразрядной конъюнкции к заданному IP-адресу узла и маске.<br>
    Например, если IP-адрес узла равен {host}, а маска равна {netmask}, то адрес сети равен {network}.<br>'''.format(**{'host': self.latex(sample.host()), 'netmask': self.latex(sample.netmask()), 'network': self.latex(sample.network())})
