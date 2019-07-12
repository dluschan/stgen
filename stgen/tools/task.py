from .tag import create_tag
from .program_io import generate_input
from abc import abstractmethod
from hashlib import sha1
import hmac
import subprocess
import os


class BaseTask:
	"""Базовый класс для задач"""
	@abstractmethod
	def question_text(self):
		"""Возвращает текст вопроса."""

	@abstractmethod
	def question_answer(self):
		"""Возвращает ответ на вопрос."""

	def get_type_tag(self):
		"""Возвращает категорию вопроса."""
		question = create_tag('question', None, {"type": "category"})
		category = create_tag('category')
		text = create_tag('text', self.category())
		category.appendChild(text)
		question.appendChild(category)
		return question

	def get_task_tag(self):
		"""Возвращает вопрос."""
		task = self.question_text()
		question = create_tag('question', None, {"type": self.question_type()})
		name = create_tag('name')
		text = create_tag('text', 'Задача №' + self.sha1(str(task)))
		name.appendChild(text)
		question.appendChild(name)
		question_text = create_tag('questiontext', None, {"format": "html"})
		text = create_tag('text', self.question_text(), cdata = self.cdata())
		question_text.appendChild(text)
		question.appendChild(question_text)
		answer = create_tag('answer', None, {"fraction": "100", "format": "moodle_auto_format"})
		text = create_tag('text', str(self.question_answer()))
		answer.appendChild(text)
		question.appendChild(answer)
		return question

	@staticmethod
	def question_type():
		"""Тип вопроса.

		Возможные значения: «numerical», «shortanswer» и другие. По умолчанию «shortanswer»."""
		return 'shortanswer'

	@staticmethod
	def cdata():
		return False

	@staticmethod
	def sha1(text):
		assert(type(text) == str)
		return hmac.new(bytearray(text, 'utf-8'), bytearray('text', 'utf-8'), sha1).hexdigest()

	@staticmethod
	def latex(element):
		return '\\( ' + str(element) + ' \\)'

	@staticmethod
	def category():
		return '$course$/ЕГЭ/'


class CodeRunnerTask(BaseTask):
	@abstractmethod
	def question_text(self):
		"""Возвращает текст вопроса."""

	@abstractmethod
	def question_answer(self):
		"""Возвращает ответ на вопрос."""

	def get_task_tag(self):
		"""Возвращает вопрос."""
		task = self.question_text()
		question = create_tag('question', None, {"type": self.question_type()})
		name = create_tag('name')
		text = create_tag('text', 'Задача №' + self.sha1(str(task)))
		name.appendChild(text)
		question.appendChild(name)
		question_text = create_tag('questiontext', None, {"format": "html"})
		text = create_tag('text', self.question_text(), cdata=self.cdata())
		question_text.appendChild(text)
		question.appendChild(question_text)
		coderunnertype_tag = create_tag('coderunnertype', 'multilanguage')
		question.appendChild(coderunnertype_tag)
		testcases_tag = create_tag('testcases')
		with open("solver.py", "w") as solver_file:
			solver_file.write(self.solver)
		for sample in self.input_samples:
			testcase_tag = create_tag('testcase', None, {
				'testtype': "0", 'useasexample': "1", 'hiderestiffail': "0", 'mark': "1.0000000"
			})
			stdin_tag = create_tag('stdin')
			with open("input.txt", "w") as input_file:
				input_file.write(sample)
			test_output = subprocess.Popen(
				"""python3 solver.py < input.txt""",
				shell=True,
				stdout=subprocess.PIPE
			).stdout.read().decode('utf-8')
			stdin_tag.appendChild(create_tag('text', sample))
			expected_tag = create_tag('expected')
			expected_tag.appendChild(create_tag('text', test_output))
			display_tag = create_tag("display")
			display_tag.appendChild(create_tag("text", "SHOW"))
			testcase_tag.appendChild(stdin_tag)
			testcase_tag.appendChild(expected_tag)
			testcase_tag.appendChild(display_tag)
			testcases_tag.appendChild(testcase_tag)
		for i in range(self.test_size - len(self.input_samples)):
			sample = generate_input(self.input_format, self.params)
			testcase_tag = create_tag('testcase', None, {
				'testtype': "0", 'useasexample': "0", 'hiderestiffail': "0", 'mark': "1.0000000"
			})
			stdin_tag = create_tag('stdin')
			with open("input.txt", "w") as input_file:
				input_file.write(sample)
			test_output = subprocess.Popen(
				"""python3 solver.py < input.txt""",
				shell=True,
				stdout=subprocess.PIPE
			).stdout.read().decode('utf-8')
			stdin_tag.appendChild(create_tag('text', sample))
			expected_tag = create_tag('expected')
			expected_tag.appendChild(create_tag('text', test_output))
			display_tag = create_tag("display")
			display_tag.appendChild(create_tag("text", "SHOW"))
			testcase_tag.appendChild(stdin_tag)
			testcase_tag.appendChild(expected_tag)
			testcase_tag.appendChild(display_tag)
			testcases_tag.appendChild(testcase_tag)
		os.remove("input.txt")
		os.remove("solver.py")
		question.appendChild(testcases_tag)
		return question

	@staticmethod
	def question_type():
		"""Тип вопроса.

		Возможные значения: «numerical», «shortanswer» и другие. По умолчанию «shortanswer»."""
		return 'coderunner'

	def category(self):
		return super().category()

