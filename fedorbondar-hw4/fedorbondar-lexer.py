import ply.lex as lex
import sys

tokens = [
    'TERMINAL',
    'NOT_A_TERMINAL',
    'FIRST_NOT_A_TERMINAL',
    'BIND',
    'OR',
    'ENDL',
    'NULL'
]


t_BIND = r'~'
t_OR = r'\|'
t_ENDL = r','
t_NULL = r'NULL'

t_ignore = " \t\r\f"


def drop_commas_and_backslash(s):
    return s.replace("\\" + '"', '"').replace("\\" + "\\", "\\")


def t_TERMINAL(t):
    r'\'.+?(?<!\\)\''
    t.value = drop_commas_and_backslash(t.value[1:-1])
    return t


def t_NOT_A_TERMINAL(t):
    r'\".+?(?<!(?<!\\)\\)\"'
    t.value = drop_commas_and_backslash(t.value[1:-1])
    return t


def t_FIRST_NOT_A_TERMINAL(t):
    r'first~\".+?(?<!(?<!\\)\\)\"'
    t.value = drop_commas_and_backslash(t.value[7:-1])
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character " + str(t.value[0]) + " in line " + str(t.lexer.lineno))
    t.lexer.skip(1)


def main():
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])

        with open(filename, 'r') as code, open(filename + ".out", "w") as outfile:
            lexer = lex.lex()
            lexer.input("".join(code.readlines()))

            while True:
                tok = lexer.token()
                if not tok:
                    break
                print(tok, file=outfile)


if __name__ == "__main__":
    main()
