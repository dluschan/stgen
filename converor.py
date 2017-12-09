from xml.dom import minidom
import sys, json

def create_tag(name: str=None, text: str=None, attributes: dict=None, *, cdata: bool=False):
    doc = minidom.Document()

    if name is None:
        return doc

    tag = doc.createElement(name)

    if text is not None:
        if cdata is True:
            tag.appendChild(doc.createCDATASection(text))
        else:
            tag.appendChild(doc.createTextNode(text))

    if attributes is not None:
        for k, v in attributes.items():
            tag.setAttribute(k, str(v))

    return tag

j = json.loads(input())

doc = create_tag()

quiz = create_tag('quiz')
doc.appendChild(quiz)

question = create_tag('question', None, {"type": "category"})
category = create_tag('category')
text = create_tag('text', j["category"])
category.appendChild(text)
question.appendChild(category)
quiz.appendChild(question)

for q in j["questions"]:
    question = create_tag('question', None, {"type": j["question_type"]})
    name = create_tag('name')
    text = create_tag('text', q["question_name"])
    name.appendChild(text)
    question.appendChild(name)
    
    questiontext = create_tag('questiontext', None, {"format": "html"})
    text = create_tag('text', "<p>" + q["question_text"] + "</p>" + "<p><img src=\"data:image/png;base64," + q["question_media"] + "\"></p>", cdata = True)
    questiontext.appendChild(text)
    question.appendChild(questiontext)

    answer = create_tag('answer', None, {"fraction": "100", "format": "moodle_auto_format"})
    text = create_tag('text', str(q["question_answer"]))
    answer.appendChild(text)
    question.appendChild(answer)
    quiz.appendChild(question)

print(doc.toprettyxml(indent="  "))
