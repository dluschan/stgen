from abc import abstractmethod


class Information:
	def __init__(self, value):
		self.value = value

	@abstractmethod
	def __abs__(self):
		"""перевести количество информации в биты"""

	def __eq__(self, other):
		assert isinstance(other, Information)
		return abs(self) == abs(other)

	def __lt__(self, other):
		assert isinstance(other, Information) or (isinstance(other, Prefix) and isinstance(other.value, Information))
		return abs(self) < abs(other)


class Bit(Information):
	def __abs__(self):
		return self.value


class Byte(Information):
	def __abs__(self):
		return self.value * 8


class Time:
	def __init__(self, value):
		self.value = value

	@abstractmethod
	def __abs__(self):
		"""перевести время в секунды"""

	def __eq__(self, other):
		assert isinstance(other, Time)
		return abs(self) == abs(other)

	def __lt__(self, other):
		assert isinstance(other, Time)
		return abs(self) < abs(other)


class Second(Time):
	def __abs__(self):
		return self.value


class Minute(Time):
	def __abs__(self):
		return self.value * 60


class Hour(Time):
	def __abs__(self):
		return self.value * 60 * 60


class Prefix:
	def __init__(self, value):
		self.value = value

	@abstractmethod
	def __abs__(self):
		"""посчитать значение величины"""

	def __eq__(self, other):
		#assert проверить, что ближайший общий предок не object
		return abs(self) == abs(other)

	def __lt__(self, other):
		#assert проверить, что ближайший общий предок не object
		return abs(self) < abs(other)


class BinaryPrefix(Prefix):
	def __abs__(self):
		return 2**self.degree * abs(self.value)


class kibi(BinaryPrefix):
	degree = 10


class mebi(BinaryPrefix):
	degree = 20


class gibi(BinaryPrefix):
	degree = 30
