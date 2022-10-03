import ply.lex as lex
import sys

tokens = [
    'START',
    'LBR',
    'RBR',
    'TERMINAL',
    'NON_TERMINAL',
    'EMPTY',
    'EQUAL',
    'SEPARATOR'
]

t_START = r'STARTING_NON_TERMINAL'
t_EQUAL = r'='
t_LBR = r'\{'
t_RBR = r'\}'
t_SEPARATOR = r';'
t_EMPTY = r'EPS'
t_ignore = ' \t'


def t_TERMINAL(t):
    r'"[^"]+"'
    t.value = t.value[1:-1]
    return t


def t_NON_TERMINAL(t):
    r'\$[^\$]\$'
    t.value = t.value[1:-1]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def main():
    if len(sys.argv) != 2:
        print(f"Error. Expected 2, received {len(sys.argv) - 1}")
        exit(1)

    lexer = lex.lex()

    file_name = sys.argv[1]
    sys.stdout = open(file_name + '.out', 'w')

    with open(file_name, 'r') as cin:
        lexer.input(' '.join(cin.readlines()))
        while True:
            t = lexer.token()
            if not t:
                break
            print(t)


if __name__ == "__main__":
    main()
