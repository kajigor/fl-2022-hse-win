import ply.lex as lex
import sys

tokens = [
    'START',
    'TERM',
    'NON_TERM',
    'RULE',
]

t_RULE = r'\->'
t_START = r'=>'

escapes = {'\@': '@',
           '\&': '&',
           '\\\\': '\\'}


def clear_escapes(line):
    for char in escapes:
        line = line.replace(char, escapes[char])
    return line


def t_TERM(t):
    r'@(([^\\]*?)|\\.)*?@'
    t.value = clear_escapes(t.value[1:-1])
    return t


def t_NON_TERM(t):
    r'&(([^\\]*?)|\\.)*?&'
    t.value = clear_escapes(t.value[1:-1])
    return t


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def lex_from_file(file):
    sys.stdout = open(file + '.out', mode='w')
    lexer.input(open(file, mode='r').read())

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


def main():
    lex_from_file(sys.argv[1])


if __name__ == "__main__":
    main()
