from setuptools import setup, find_packages

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='stgen',
	version='0.3.1',
	author='Dmitry Luschan',
	author_email='dluschan@gmail.com',
	description='School tasks generator',
	long_description=long_description,
	url='https://github.com/dluschan/stgen',
	packages=find_packages(),
	keywords='ЕГЭ информатика',
	install_requires=['urwid', 'ply'],
	test_suite='tests',
	entry_points={
		'console_scripts': [
			'stgen = stgen.tui.tui:main'
		],
	},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Topic :: Education :: Testing",
		"Natural Language :: Russian",
		"Development Status :: 4 - Beta",
		"Environment :: Console :: Curses",
	],
)
