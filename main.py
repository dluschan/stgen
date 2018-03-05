import urwid
from .generator import BaseGenerator, MainGenerator

def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in all_subclasses(s)]

choices = list(filter(lambda g: g.__subclasses__() == [], all_subclasses(BaseGenerator)))
choices_list = list(map(str, choices))
choiced = {}

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        checkbox = urwid.CheckBox(c)
        urwid.connect_signal(checkbox, 'change', item_chosen, c)
        body.append(urwid.AttrMap(checkbox, None, focus_map='reversed'))
    body.append(urwid.Divider())
    body.append(urwid.Button('Ok'))
    urwid.connect_signal(body[-1], 'click', click_ok, body[-1])
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def process(button, output):
    print(MainGenerator(choiced).generate(), file = open(output.get_edit_text(), 'w'))

def click_ok(checkbox, button):
    response = urwid.Edit('Enter output filename: ', 'output.xml')
    done_btn = urwid.Button('Exit')
    urwid.connect_signal(done_btn, 'click', exit_program)
    ok_btn = urwid.Button('Generate')
    urwid.connect_signal(ok_btn, 'click', process, response)
    main.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(ok_btn, None, focus_map='reversed'), urwid.AttrMap(done_btn, None, focus_map='reversed')]))

def item_chosen(checkbox, choice, param):
    choiced[choices[choices_list.index(param)]] = choice

def exit_program(button):
    raise urwid.ExitMainLoop()

main = urwid.Padding(menu('Question types', choices_list), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
