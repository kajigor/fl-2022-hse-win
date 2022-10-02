import ply.lex as lex
import sys

tokens = [
    'TERM',
    'NO_TERM',
    'TRANSITION',
    'OR',
    'EPS',
    'INITIAL',
    'END'
]

t_OR = r'\|'
t_TRANSITION = r'-->'
t_EPS = r'EPS'
t_END = r';'
t_ignore = " \t"


def cut_out(line):
    return line.replace("\\" + '"', '"').replace("\\" + "\\", "\\")


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character " + str(t.value[0]) + " on line " + str(t.lexer.lineno))
    t.lexer.skip(1)

def t_TERM(t):
    r'".+?(?<!\\)"'
    t.value = cut_out(t.value[1:-1])
    return t


def t_NO_TERM(t):
    r'<.+?(?<!(?<!\\)\\)>'
    t.value = cut_out(t.value[1:-1])
    return t


def t_INITIAL(t):
    r'initial--<.+?(?<!(?<!\\)\\)>'
    t.value = cut_out(t.value[10:-1])
    return t


lexer = lex.lex()


def main():
    filename: str = sys.argv[1]
    with open(filename, 'r') as code, open(filename + ".out", "w") as answer:
        lexer = lex.lex()
        lexer.input("".join(code.readlines()))
        while token := lexer.token():
            print(token, file=answer)


if __name__ == "__main__":
    main()
