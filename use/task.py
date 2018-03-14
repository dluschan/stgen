import hmac, hashlib
from .tag import create_tag

class BaseTask:
    '''Базовый класс для задач'''
    def get_type_tag(self):
        question = create_tag('question', None, {"type": "category"})
        category = create_tag('category')
        text = create_tag('text', self.category())
        category.appendChild(text)
        question.appendChild(category)
        return question

    def get_task_tag(self):
        task = self.question_text()
        question = create_tag('question', None, {"type": self.question_type()})
        name = create_tag('name')
        text = create_tag('text', 'Задача №' + self.sha1(str(task)))
        name.appendChild(text)
        question.appendChild(name)
        questiontext = create_tag('questiontext', None, {"format": "html"})
        text = create_tag('text', self.question_text(), cdata = self.cdata())
        questiontext.appendChild(text)
        question.appendChild(questiontext)
        answer = create_tag('answer', None, {"fraction": "100", "format": "moodle_auto_format"})
        text = create_tag('text', str(self.question_answer()))
        answer.appendChild(text)
        question.appendChild(answer)
        return question

    def question_type(self):
        return 'shortanswer'

    def cdata(self):
        return False

    def sha1(self, text):
        assert(type(text) == str)
        return hmac.new(bytearray(text, 'utf-8'), bytearray('text', 'utf-8'), hashlib.sha1).hexdigest()

    def latex(self, element):
        return '\( ' + str(element) + ' \)'

    def category(self):
        return '$course$/ЕГЭ/'

