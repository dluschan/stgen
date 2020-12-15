class Audio:
	def __init__(self, duration, frequency, word_size, channels):
		self.duration = duration
		self.frequency = frequency
		self.word_size = word_size
		self.channels = channels
		self.volume = self.duration * self.frequency * self.word_size * self.channels

	def size(self):
		return self.volume


class Image:
	def __init__(self, w, h, bit):
		self.w = w
		self.h = h
		self.bit = bit

	def colors(self):
		return 2 ** self.bit

	def size(self):
		return self.w * self.h * self.bit

