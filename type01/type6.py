from ..notation import transform
from random import randint, choice
from ..tag import create_tag
from .generator import Generator_01

class Generator_01_type_1(Generator_01):
    'Идея задачи: использование сдвига вместо деления и умножения.'

    def __init__(self):
        self.question = 'Найдите значение выражение {expression}. Ответ запишите в системе счисления с основанием {base}.'
        self.m = 8
        self.source_base = randint(2, 9)
        self.limit_base = {2: 5, 3: 3, 4: 2, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1}
        self.limit_factor = {2: 8, 3: 5, 4: 4, 5: 3, 6: 3, 7: 3, 8: 2, 9: 2}
        self.target_base = self.source_base ** randint(1, self.limit_base[self.source_base])
        self.k = randint(2, 3)
        self.terms = [[randint(10**(self.m-1), 10**(self.m+1)), randint(1, self.limit_base[self.source_base]), randint(2, self.limit_factor[self.source_base]), choice([self.div, self.prod]), choice([+1, -1])] for _ in range(self.k)]
        for i in range(self.k):
            if self.terms[i][3] == self.prod:
                self.terms[i][0] = self.terms[i][0] // (self.source_base ** self.terms[i][2]) * (self.source_base ** self.terms[i][2])
        if self.value(self.terms) < 0:
            self.terms = [[term[0], term[1], term[2], term[3], -1*term[4]] for term in self.terms]
        while self.terms[0][4] < 0:
            self.terms.append(self.terms.pop(0))

    def category(self):
        return super(Generator_01_type_1, self).category() + 'Тип 6'

    def question_text(self):
        expression = ' '.join([self.convert(*p, self.source_base) for p in self.terms])[2:]
        return self.question.format(expression = self.latex(expression), base = self.latex(self.target_base))

    def div(self, x, k, base):
        return x * (base ** k) + randint(0, base ** k - 1)

    def prod(self, x, k, base):
        return x // (base ** k)

    def convert(self, x, m, k, f, s, base):
        sings = {+1: '+ ', -1: '- ', self.div: ' \\div ', self.prod: ' \\times '}
        params = ['\\text' + '{' + transform(f(x, k, base), base ** m) + '}' + '_' + '{' + str(base**m) + '}', str(base**k)]
        return sings[s] + sings[f].join(params)

    def value(self, terms):
        return sum([p[0] * p[4] for p in terms])

    def question_answer(self):
        return transform(self.value(self.terms), self.target_base)
