import argparse
from .tui import tui
from .tools.generator import MainGenerator
from .tools.task import BaseTask, CodeRunnerTask


def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in all_subclasses(s)]


def createParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    batch_parser = subparsers.add_parser('batch')
    batch_parser.add_argument('--task', '-t', nargs='+', type=int, required=True)
    batch_parser.add_argument('--count', '-c', type=int, required=True)
    batch_parser.add_argument('--output', '-o', type=argparse.FileType(mode='w', bufsize=-1, encoding=None, errors=None), required=True)
    interactive_parser = subparsers.add_parser('tui')
    return parser


def batch(namespace):
    choiced = []
    clses = {cls.__name__.split('.')[1] if cls.__name__.count('.') else cls.__name__: cls for cls in BaseTask.__subclasses__() + CodeRunnerTask.__subclasses__()}
    for t in namespace.task:
        class_name = 'Task' + str(t).zfill(2)
        choiced += [g for g in all_subclasses(clses[class_name]) if g.__subclasses__() == []]
    print(MainGenerator(choiced).generate(namespace.count), file=namespace.output)


def main():
    parser = createParser()
    namespace = parser.parse_args()
    if namespace.command == "tui":
        return tui.main()
    elif namespace.command == "batch":
        return batch(namespace)
    else:
        parser.print_help()
