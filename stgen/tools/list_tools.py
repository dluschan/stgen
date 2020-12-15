"""Вспомогательные функции для манипулирования списками."""

from random import choices, sample


def pairs(s, k):
	"""Возвращает k пар подряд стоящих элементов списка s."""
	assert len(s) > k
	for i in sample(range(len(s) - 1), k):
		yield s[i: i + 2]


def split(s, k):
	"""Разбивает список s на k непустых списка."""
	assert len(s) >= k
	mid = sorted(sample(range(1, len(s) - 1), k - 1))
	for left, right in zip([0] + mid, mid + [len(s)]):
		yield s[left: right]


def align(x, y):
	"""Выравнивает длины списков с помощью случайного повтора элементов короткого."""
	return x + choices(x, k=max(len(y) - len(x), 0)), y + choices(y, k=max(len(x) - len(y), 0))
