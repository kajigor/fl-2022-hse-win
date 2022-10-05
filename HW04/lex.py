import ply.lex as lex
import sys

tokens = [
    "EQ",
    "EPS",
    "UNION",
    "ENDL",
    "TERM",
    "NON_TERM",
    "START"
]

t_UNION = r'\|'
t_EPS = r'EPS'
t_ENDL = r';'
t_EQ = r'='

t_ignore = ' \t'


def remove_shields(exp):
    return exp.replace("\\" + "\\", "\\").replace("\\" + "$", "$").replace("\\" + "'", "'")


def t_START(t):
    r'START\(\$(\S+(?<!(?!<\\)\\|\$))\);'
    t.value = remove_shields(t.value[7:-2])
    return t


def t_TERM(t):
    r'\'.+?(?<!\\)\''
    t.value = remove_shields(t.value[1:-1])
    return t


def t_NON_TERM(t):
    r'\$(\S+(?<!(?!<\\)\\|\$|;))'
    t.value = remove_shields(t.value[1:])
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def main():
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])

        with open(filename, 'r') as fin, open(filename + ".out", "w") as fout:
            lexer.input("".join(fin.readlines()))

            while True:
                tok = lexer.token()
                if not tok:
                    break
                print(tok, file=fout)


if __name__ == "__main__":
    main()