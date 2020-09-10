from .common import Task27

class Type2(Task27):
	def __init__(self):
		super().__init__()
		self.test_size = 25
		self.params = {
			'n': [int, [2, 10], 'количество чисел'],
			's': [int, None, 'искомая сумма'],
			'x': [int, [-100, 100], 'число в последовательности'],
		}
		self.legend = f"""Имеется последовательность целых чисел.
		Необходимо найти максимальную чётную сумму чисел этой последовательности."""
		self.solver = f"""pos_sum = 0
pos_min_odd = None
neg = [[], []]
neg_limit = [1, 2]

n = int(input())
for i in range(n):
	x = int(input())
	if x > 0:
		pos_sum += x
		if x % 2 != 0 and (pos_min_odd is None or x < pos_min_odd):
			pos_min_odd = x
	else:
		neg[x % 2].append(x)
		neg[x % 2].sort()
		if len(neg[x % 2]) > neg_limit[x % 2]:
			neg[x % 2].pop(0)

candidate = []
if neg[0]:
	candidate.append(neg[0][0])
if len(neg[1]) > 1:
	candidate.append(sum(neg[1]))
if pos_sum:
	candidate.append(pos_sum)
	if neg[1]:
		candidate.append(pos_sum + neg[1][-1])
	if pos_min_odd and pos_sum > pos_min_odd:
		candidate.append(pos_sum - pos_min_odd)

print(max(filter(lambda x: x % 2 == 0, candidate)))
"""
		self.input_format = """n
x|n"""
		self.output_format = """s"""
		self.input_samples = ["""4
4
5
6
7
""",
"""3
1
2
-3
""",
"""3
11
2
-3
""",
"""2
1
-3
""",
"""3
3
2
-3
""",
"""3
5
1
-3
""",
"""3
5
0
-3
""",
"""3
5
0
-7
""",
"""2
5
-5
""",
"""3
5
5
5
""",
"""3
-1
-2
-3
""",
"""3
-1
0
-3
""",
"""3
-1
-1
-8
""",
"""3
-1
-2
0
""",
"""7
6
2
0
3
-1
-2
-3
""",
"""4
-1
-1
2
-2
""",
"""4
-7
-7
9
-2
""",
"""2
0
1
""",
"""2
0
2
""",
"""2
0
-2
""",
"""2
-1
-2
""",
"""2
-1
-3
""",
"""2
0
-1
""",
]

	def category(self):
		return super().category() + 'Тип 2'

