import ply.lex as lex
import sys

tokens = [
    'TERMINAL',
    'NOT_TERMINAL',
    'START',
    'EMPTY',
    'IS',
    'END_LINE',
    'OR'
]

t_IS = r'->'
t_EMPTY = r'\#'
t_END_LINE = r';'
t_OR = r'\|'
t_ignore = r' '


def t_START(t):
    r'start->\%([^\\\$\%\#] | \\.)*?\%'
    t.value = t.value[7:-1].replace("\\$", "$").replace("\\%", "%").replace("\\#", "#").replace("\\\\", "\\")
    return t


def t_NOT_TERMINAL(t):
    r'\%([^\\\$\%\#] | \\.)*?\%'
    t.value = t.value[1:-1].replace("\\$", "$").replace("\\%", "%").replace("\\#", "#").replace("\\\\", "\\")
    return t


def t_TERMINAL(t):
    r'\$([^\\\$\%\#] | \\.)*?\$'
    t.value = t.value[1:-1].replace("\\$", "$").replace("\\%", "%").replace("\\#", "#").replace("\\\\", "\\")
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()


def main():
    lexer = lex.lex()
    infile = sys.argv[1]
    with open(infile) as file:
        for line in file:
            lexer.input(line)
            while True:
                tok = lexer.token()
                if not tok:
                    break
                print(tok)


if __name__ == "__main__":
    main()
