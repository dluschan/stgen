from ..tools.task import CodeRunnerTask
from ..tools.program_io import parse_input, parse_output


class Task27(CodeRunnerTask):
	def __init__(self):
		super().__init__()

	def question_text(self):
		return self.legend + "\n" + parse_input(self.input_format, self.params) + "\n" + parse_output(self.output_format, self.params)

	def category(self):
		return super().category() + 'Задача 27/'

