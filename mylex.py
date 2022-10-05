import ply.lex as lex
import sys

tokens = [
    'TERMINAL',
    'NON_TERMINAL',
    'START',
    'NONE',
    'ARROW',
    'SEPARATOR',
    'ALTERNATIVE'
]

t_ARROW = r'='
t_NONE = r'@'
t_SEPARATOR = r';'
t_ALTERNATIVE = r'\|'
t_ignore = " \t"


def change(name):
    return name.replace("\\$", "$").replace("\\&", "&").replace("\\\\", "\\")


def t_START(t):
    r'start=\$([^\\\&\$@] | \\.)*?\$'
    t.value = change(t.value[7:-1])
    return t


def t_TERMINAL(t):
    r'\&([^\\\&\$@] | \\.)*?\&'
    t.value = change(t.value[1:-1])
    return t


def t_NON_TERMINAL(t):
    r'\$([^\\\&\$@] | \\.)*?\$'
    t.value = change(t.value[1:-1])
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
    outfile = infile + ".out"
    with open(infile, 'r') as lang, open(outfile, 'w') as result:
        for line in lang:
            lexer.input(line)
            while True:
                tok = lexer.token()
                if not tok:
                    break
                result.write(str(tok) + "\n")


if __name__ == "__main__":
    main()
