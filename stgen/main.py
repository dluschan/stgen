"""
usage: stgen batch -t 7 12 -c 1500 -o output.xml
usage: stgen tui
"""
import argparse
from .tui import tui
from .tools.generator import MainGenerator


def createParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    batch_parser = subparsers.add_parser('batch')
    batch_parser.add_argument('-t', nargs='+', type=int)
    batch_parser.add_argument('-c', type=int)
    batch_parser.add_argument('-o', type=argparse.FileType(mode='w', bufsize=-1, encoding=None, errors=None))
    interactive_parser = subparsers.add_parser('tui')
    return parser


def batch(namespace):
    return 0
    choiced = ['Task']
    print(MainGenerator(choiced).generate(10), file=open(output.get_edit_text(), 'w'))


def main():
    parser = createParser()
    namespace = parser.parse_args()
    if namespace.command == "tui":
        return tui.main()
    elif namespace.command == "batch":
        return batch(namespace)
    else:
        parser.print_help()
