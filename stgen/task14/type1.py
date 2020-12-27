from random import choice, choices, randrange, randint, sample
from .common import Task14
from ..tools.common import hex_digits


class Type1(Task14):
	"""Исполнитель редактор."""
	def __init__(self):
		super().__init__()
		self.letters = sample(hex_digits, 2)
		self.repeats = randint(50, 500)
		self.src = choice(self.letters)
		x = sorted(sample(range(1, 8), k=4), reverse=True)
		self.args = [self.letters[a] * b for a, b in zip((0, 1, 0, 0, 1, 1, 0), (x[0], x[1], x[0], x[0], x[2], x[1], x[3]))]
		self.algo = """while find('{}') or find('{}'):
    if find('{}'):
        replace('{}', '{}')
    else:
        replace('{}', '{}')""".format(*self.args)
		self.question = f"""<p>Какая строка получится в результате применения приведённой ниже программы к строке, состоящей из {self.repeats} идущих подряд символов '{self.src}'? В ответе запишите полученную строку.</p>
<h4>Программа:</h4>
<p><pre><code>{self.algo}</code></pre></p>
"""

	def category(self):
		return super().category() + 'Тип 1/'

	def question_text(self):
		return self.question

	def question_answer(self):
		s = self.src * self.repeats
		def replace(a, b):
			nonlocal s
			s = s.replace(a, b, 1)
		find = lambda q: q in s
		exec(self.algo)
		return s


class SubtypeA(Type1):
	"""Исполнитель редактор, который заменяет простые строки из одной буквы."""
	def __init__(self):
		super().__init__()

	def category(self):
		return super().category() + 'Подтип A'
