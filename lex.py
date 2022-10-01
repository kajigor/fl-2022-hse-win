import ply.lex as lex
import sys

tokens = [
    'TERM',
    'NTERM',
    'STARTTERM',
    'EPSILON',
    'SEPARATOR',
    'ARROW'
]


def t_TERM(t):
    r'α[\x00-\x7F]+α'
    t.value = t.value[1:-1]
    return t

def t_NTERM(t):
    r'β[\x00-\x7F]+β'
    t.value = t.value[1:-1]
    return t

def t_STARTTERM(t):
    r'γ[\x00-\x7F]+γ'
    t.value = t.value[1:-1]
    return t

t_EPSILON = r'ε'
t_ARROW = r'→'
t_SEPARATOR = r'±'
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def test(lexer):
    tests = ["arithmetic", "brackets", "palindromes"]
    for cur_test in tests:
        with open("tests_and_examples/" + cur_test + ".txt", "r") as f:
            with open("tests_and_examples/" + cur_test + ".lex.ans", "r") as f1:
                res = ''
                for line in f.readlines():
                    lexer.input(line)
                    while True:
                        tok = lexer.token()
                        if not tok:
                            break
                        res += str(tok) + '\n'
                lines = f1.readlines()
                lines1 = str(res).split('\n')[:-1]
                assert len(lines) == len(lines1)
                for i in range(len(lines)):
                    assert lines[i] == lines1[i] + '\n'
                lexer.lineno = 1

def main():
    lexer = lex.lex()

    test(lexer)

    with open(sys.argv[1], "r") as f:
        with open(sys.argv[1] + ".out", "w") as f1:
            for line in f.readlines():
                lexer.input(line)
                while True:
                    tok = lexer.token()
                    if not tok:
                        break
                    f1.write(str(tok) + '\n')


if __name__ == "__main__":
    main()
