"""
Модуль для неравномерного кодирования информации.
"""
from huffman import codebook


def code(terms, frequency=None):
	if not frequency:
		frequency = [1] * len(terms)
	return codebook(zip(terms, frequency))
