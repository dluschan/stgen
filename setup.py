from setuptools import setup, find_packages

setup(
	name='use',
	version='0.1.0',
	author='Dmitry Luschan',
	author_email = 'dluschan@gmail.com',
	description='Package for generate questions for informatics USE (moodle format).',
	long_description='',
	url='https://github.com/dluschan/use',
	packages=find_packages(),
	keywords='info informatics use exam',
	install_requires=['urwid', 'ply'],
	test_suite='tests',
	entry_points={
		'console_scripts': [
			'use = use.tui.tui:main'
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
