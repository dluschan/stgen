from .common import *

class Type0(Task18):
    '''Определение искомого отрезка.'''
    def __init__(self):
        super().__init__()
        self.question = 'На числовой прямой даны два отрезка: P = [17, 40] и Q = [20, 57]. Отрезок A таков, что приведённая ниже формула истинна при любом значении переменной х:'
        self.number = randint(self.base, self.base ** 2 - 1)

    def category(self):
        return super().category() + 'Тип 0'

    def question_text(self):
        return self.question.format(number = self.latex(self.number), view = self.latex(transform(self.number, self.base)))

    def question_answer(self):
        return self.base

