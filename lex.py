import ply.lex as lex
import sys

tokens = [
    'TERMINAL',
    'NON_TERMINAL',
    'START_TOKEN',
    'LINE_SEPARATOR'
]

terminals = set()
nonTerminals = set()


def t_TOKEN(t):
    r'[^\n\s\t\r]+'
    if t.lexer.lineno == 1:
        t.type = 'TERMINAL'
        terminals.add(t.value)
    elif t.lexer.lineno == 2:
        t.type = 'NON_TERMINAL'
        nonTerminals.add(t.value)
    elif t.lexer.lineno == 3:
        t.type = 'START_TOKEN'
    else:
        if t.value in terminals:
            t.type = 'TERMINAL'
        elif t.value in nonTerminals:
            t.type = 'NON_TERMINAL'
        else:
            print('Illegal token: \'' + t.value + '\' on line ' + str(t.lexer.lineno))
            exit(0)

    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\s', ' ')
    t.value = t.value.replace('\\h', '\\')
    return t


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.type = 'LINE_SEPARATOR'
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    exit(0)


lexer = lex.lex()


def main():
    filename = sys.argv[1]
    output = open(filename + '.out', 'w+')
    data = open(filename).read()
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        output.write(str(tok))
        output.write('\n')


if __name__ == "__main__":
    main()
