from setuptools import setup, find_packages

setup(
    name = 'use',
    version = '0.1',
    packages = find_packages(),
    author = 'Dmitry Luschan',
    author_email = 'dluschan@gmail.com',
    keywords = 'info informatics use exam',
    description = 'Package for generate questions for informatics USE (moodle format).',
    install_requires = ['urwid'],
    test_suite = 'tests',
)
