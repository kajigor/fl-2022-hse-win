import ply.lex as lex
import sys

output_file = None
error = False
tokens = [
    'TERMINAL',
    'NOT_TERMINAL',
    'INITIAL',
    'IMPLICATION',
    'ALTERNATIVE',
    'EPSILON'
]


def t_NOT_TERMINAL(t):
    r'\«.+?»'
    t.value = str(t.value[1:-1])
    return t


def t_TERMINAL(t):
    r'⌊.+?⌋'
    t.value = str(t.value[1:-1])
    return t


def t_INITIAL(t):
    r'initial_not_terminal=«.+?»'
    t.value = str(t.value[22:-1])
    return t


t_IMPLICATION = r'->'

t_ALTERNATIVE = r'\|'

t_EPSILON = r'EPS'

t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    global error, output_file
    print(f"Lexical error in '%s' at line {t.lexer.lineno}" % t.value[0], file=output_file)
    t.lexer.skip(len(t.value))

    error = True


lexer = lex.lex()


def main():
    file_name = sys.argv[1]
    global output_file
    output_file = open(file_name + ".out", 'w')
    with open(file_name, "r") as file:
        for line in file:
            lexer.input(line)
            while not error:
                tok = lexer.token()
                if not tok:
                    break
                print(tok, file=output_file)


if __name__ == "__main__":
    main()
