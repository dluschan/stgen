"""Синтаксический разбор логических уравнений.

Скобки используются для повышения приоритета и явно остаются в выражении.
"""

from ..tools.boolean import *
import ply.lex as lex
import ply.yacc as yacc


tokens = (
	'TERM',
	'FALSE', 'TRUE',
	'NEGATION', 'CONJUNCTION', 'DISJUNCTION', 'IMPLICATION', 'EQUAL', 'NOTEQUAL',
	'LPAREN', 'RPAREN'
)

# Tokens
t_TERM        = r'[a-zA-Z][0-9][0-9]*'
t_FALSE       = r'0'
t_TRUE        = r'1'
t_NEGATION    = r'!'
t_CONJUNCTION = r'&'
t_DISJUNCTION = r'\|'
t_IMPLICATION = r'->'
t_EQUAL       = r'=='
t_NOTEQUAL    = r'\!='
t_LPAREN      = '\('
t_RPAREN      = '\)'


# Ignored characters
t_ignore = " \t"


def t_newline(t):
	r"""\n+"""
	t.lexer.lineno += t.value.count("\n")


def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Parsing rules
precedence = (
	('left', 'EQUAL', 'NOTEQUAL'),
	('left', 'IMPLICATION'),
	('left', 'DISJUNCTION'),
	('left', 'CONJUNCTION'),
	('right', 'NEGATION'),
)

terms = []

def p_statement_expr(t):
	"""statement : expression"""
	t[0] = t[1]


def p_expression_neg(t):
	"""expression : NEGATION expression"""
	t[0] = Negation(t[2])


def p_expression_conj(t):
	"""expression : expression CONJUNCTION expression"""
	t[0] = Conjunction(t[1], t[3])


def p_expression_disj(t):
	"""expression : expression DISJUNCTION expression"""
	t[0] = Disjunction(t[1], t[3])


def p_expression_impl(t):
	"""expression : expression IMPLICATION expression"""
	t[0] = Implication(t[1], t[3])


def p_expression_equal(t):
	"""expression : expression EQUAL expression"""
	t[0] = Equal(t[1], t[3])


def p_expression_notequal(t):
	"""expression : expression NOTEQUAL expression"""
	t[0] = NotEqual(t[1], t[3])


def p_expression_group(t):
	"""expression : LPAREN expression RPAREN"""
	t[0] = Brackets(t[2])


def p_expression_term(t):
	"""expression : TERM"""
	t[0] = Variable(t[1])


def p_expression_false(t):
	"""expression : FALSE"""
	t[0] = FalseConst()


def p_expression_true(t):
	"""expression : TRUE"""
	t[0] = TrueConst()


def p_error(t):
	print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()


def parse(s):
	return parser.parse(s)

