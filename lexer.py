import ply.lex as lex
import sys


tokens = [
    'TERM',
    'NON_TERM',
    'EPS',
    'START',
    'DELIMITER',
    'EQ',
]

t_EPS = r'\&'
t_DELIMITER = r';'
t_EQ = r'='
t_ignore = " \t"


def my_replace(val):
    val.replace("\\$", "$").replace("\\&", "&").replace("\\\\", "\\")
    return val


def t_TERM(t):
    r'\$(([^\\<>\$])|(\\.))*?\$'
    t.value = my_replace(t.value[1:-1])
    return t


def t_NON_TERM(t):
    r'<(([^\\<>\$])|(\\.))*?>'
    t.value = my_replace(t.value[1:-1])
    return t


def t_START(t):
    r'start(\s)=(\s)<(([^\\<>\$])|(\\.))*?>'
    t.value = my_replace(t.value[9:-1])
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


def main():
    lexer = lex.lex()
    lexer.input(sys.argv[1])
    with open(sys.argv[1], "r") as input:
        with open(sys.argv[1] + ".out", "w") as output:
            for line in input.readlines():
                lexer.input(line)
                while True:
                    tok = lexer.token()
                    if not tok:
                        break
                    output.write(str(tok) + '\n')


if __name__ == "__main__":
    main()
