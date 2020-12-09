from ..tools.task import BaseTask
from functools import reduce
from random import *
from ..tools.choices import choices
import abc
import math


class Command:
	def __eq__(self, other):
		return self.__dict__ == other.__dict__

	@abc.abstractmethod
	def __hash__(self):
		pass

	@abc.abstractmethod
	def __check__(self, x):
		pass

	@abc.abstractmethod
	def __str__(self):
		pass

	@abc.abstractmethod
	def __call__(self, x):
		pass


class Addition(Command):
	"""Команда добавления к числу натурального слагаемого term."""
	def __init__(self, term=None):
		if term is None:
			term = choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [100, 70, 50, 20, 10, 2, 1, 1, 1, 1]).pop()
		self.term = term

	@abc.abstractmethod
	def __hash__(self):
		return hash(self.term)

	@abc.abstractmethod
	def check(self, x):
		return x > self.term

	@abc.abstractmethod
	def __str__(self):
		return 'Прибавить ' + str(self.term)

	@abc.abstractmethod
	def __call__(self, x):
		return x - self.term


class Multiplication(Command):
	"""Команда умножения числа на натуральный множитель factor."""
	def __init__(self, factor=None):
		if factor is None:
			factor = choices([2, 3, 4, 5, 6, 8], [100, 70, 50, 20, 10, 5]).pop()
		self.factor = factor

	@abc.abstractmethod
	def __hash__(self):
		return hash(self.factor)

	@abc.abstractmethod
	def check(self, x):
		return x % self.factor == 0

	@abc.abstractmethod
	def __str__(self):
		return 'Умножить на ' + str(self.factor)

	@abc.abstractmethod
	def __call__(self, x):
		return x // self.factor


class Power(Command):
	"""Возведение числа в натуральную степень."""
	def __init__(self, degree=None):
		if degree is None:
			degree = choices([2, 3, 4], [100, 70, 50]).pop()
		self.degree = degree

	@abc.abstractmethod
	def __hash__(self):
		return hash(self.degree)

	@abc.abstractmethod
	def check(self, x):
		return any(int(f(x ** (1/self.degree))) ** self.degree == x for f in [math.floor, math.ceil])

	@abc.abstractmethod
	def __str__(self):
		return 'Возвести в степень ' + str(self.degree)

	@abc.abstractmethod
	def __call__(self, x):
		return [int(f(x ** (1/self.degree))) for f in [math.floor, math.ceil] if f(x ** (1/self.degree)) ** self.degree == x].pop()


class Concatenation(Command):
	"""Команда дописывания справа к числу десятичной цифры."""
	def __init__(self, digit=None):
		if digit is None:
			digit = choice(range(10))
		self.digit = digit

	@abc.abstractmethod
	def __hash__(self):
		return hash(self.digit)

	@abc.abstractmethod
	def check(self, x):
		return x % 10 == self.digit

	@abc.abstractmethod
	def __str__(self):
		return 'Дописать справа цифру ' + str(self.digit)

	@abc.abstractmethod
	def __call__(self, x):
		return x // 10


class Duplication(Command):
	"""Команда дублирования последней цифры числа."""
	@abc.abstractmethod
	def check(self, x):
		return x > 9 and x % 10 == x // 10 % 10

	@abc.abstractmethod
	def __hash__(self):
		return hash(0)

	@abc.abstractmethod
	def __str__(self):
		return 'Продублировать последнюю цифру'

	@abc.abstractmethod
	def __call__(self, x):
		return x // 10


class Mechanism:
	"""Абстрактный исполнитель, который увеличивает числа с помощью разных команд."""
	def __init__(self, commands, points, exclude):
		self.commands = commands
		self.exclude = exclude
		self.points = list(sorted(points))

	def count(self, args):
		start, finish = args[0], args[1]
		d = [0] * (finish + 1)
		d[start] = 1
		for i in range(start + 1, finish + 1):
			d[i] = sum(d[command(i)] for command in self.commands if command.check(i)) if i not in self.exclude else 0
		return d[finish]

	def __call__(self):
		return reduce(lambda x, y: x * y, map(self.count, list(zip(self.points[:-1], self.points[1:]))), 1)


class Task22(BaseTask):
	"""Поиск количества способов преобразовать числа."""
	def __init__(self):
		self.mechname = choice(['РазДваТри', 'Буратино', 'ПлюсМинус', 'Тренер'])
		self.commands = {choice(Command.__subclasses__())() for _ in range(randint(2, 4))}
		self.points = {randint(2, 10)} | {randint(30, 100)} | {randint(2, 100) for _ in range(randint(0, 3))}
		self.exclude = {randint(min(self.points) + 1, max(self.points) - 1) for _ in range(randint(0, 3))} - self.points
		self.question = """Исполнитель {mechname} преобразует число на экране. У исполнителя есть {n} команды, которым 
		присвоены номера: {commands}
		Программа для исполнителя {mechname} – это последовательность команд. Сколько существует программ, которые
		преобразуют исходное число {begin} в число {end} {optional}?
		Траектория вычислений – это последовательность результатов выполнения всех команд программы."""
		self.optional = ''
		self.view = ''
		self.check()

	def check(self):
		self.res = Mechanism(self.commands, self.points, self.exclude)()
		while self.res < self.edge[0] or self.res > self.edge[1]:
			if self.res > self.edge[1]:
				self.decrease()
			else:
				self.increase()
			self.res = Mechanism(self.commands, self.points, self.exclude)()
		self.points = list(sorted(self.points))
		self.exclude = list(sorted(self.exclude))
		self.view = '<ol>' + ''.join(['<li>' + str(c) + '</li>' for c in self.commands]) + '</ol>'
		if len(self.points) == 3:
			self.optional += 'и при этом траектория вычислений содержит число ' + str(self.points[1])
		elif len(self.points) > 3:
			self.optional += 'и при этом траектория вычислений содержит числа ' + ', '.join(map(str, self.points[1:-1]))
		if len(self.exclude) == 1 and len(self.points) > 2:
			self.optional += ' и не содержит число ' + str(self.exclude[0])
		elif len(self.exclude) > 1 and len(self.points) > 2:
			self.optional += ' и не содержит числа ' + ', '.join(map(str, self.exclude))
		elif len(self.exclude) == 1 and len(self.points) == 2:
			self.optional += ' и при этом траектория вычислений не содержит число ' + str(self.exclude[0])
		elif len(self.exclude) > 1 and len(self.points) == 2:
			self.optional += ' и при этом траектория вычислений не содержит числа ' + ', '.join(map(str, self.exclude))

	def decreasecommand(self):
		self.commands.pop()

	def increasecommand(self):
		self.commands.add(choice(Command.__subclasses__())())

	def increasepoint(self):
		self.points.add(randint(2, 100))
		self.exclude -= self.points

	def decreasepoint(self):
		a = min(self.points)
		b = max(self.points)
		self.points -= {a, b}
		self.points.pop()
		self.points |= {a, b}
		self.exclude = {x for x in self.exclude if min(self.points) < x < max(self.points)}

	def increaseexclude(self):
		self.exclude.add(randint(min(self.points) + 1, max(self.points) - 1))
		self.exclude -= self.points

	def decreaseexclude(self):
		self.exclude.pop()

	def increase(self):
		f = []
		if len(self.commands) < 4:
			f.append(self.increasecommand)
		if len(self.points) > 2:
			f.append(self.decreasepoint)
		if len(self.exclude) > 1:
			f.append(self.decreaseexclude)
		if len(f) == 0:
			self.commands.pop()
		else:
			choice(f)()

	def decrease(self):
		f = []
		if len(self.commands) > 2:
			f.append(self.decreasecommand)
		if len(self.points) < 5:
			f.append(self.increasepoint)
		if len(self.exclude) < 5:
			f.append(self.increaseexclude)
		if len(f) == 0:
			self.commands.pop()
		else:
			choice(f)()

	def category(self):
		return super().category() + 'Задача 22/'

	def question_text(self):
		return self.question.format(mechname=self.mechname, n=str(len(self.commands)), commands=self.view,
									begin=self.points[0], end=self.points[-1], optional=self.optional)

	def question_answer(self):
		return self.res

	def question_type(self):
		return 'numerical'
