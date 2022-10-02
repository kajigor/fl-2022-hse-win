import ply.lex as lex
import sys

tokens = [
    'START',
    'NON_TERM',
    'TERM',
    'EPS',
    'EQUIV',
    'OR'
]

def t_START(t):
    r"\<start\>\ =\ \{(\S+(?<!(?!<\\))\\|\{|\}|\[|\])\}"
    t.value = t.value[11:-1]
    return t


def t_NON_TERM(t):
    r'\{(\S+(?<!(?!<\\)\\|\{|\}))\}'
    t.value = t.value[1:-1]
    return t


def t_TERM(t):
    r'\[(\S+(?<!(?!<\\)\\|\[|\]))\]'
    t.value = t.value[1:-1]
    return t


t_EQUIV = r'='
t_EPS = r'eps'
t_OR = r'\|'
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Unexpected character '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()


def main():
    filename = sys.argv[1]

    with open(filename, "r") as filein, open(filename + ".out", "w") as fileout:
        lexer = lex.lex()
        lexer_input = "".join(filein.readlines())
        lexer.input(lexer_input)

        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok, file = fileout)


if __name__ == "__main__":
    main()
