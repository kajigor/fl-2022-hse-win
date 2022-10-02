import ply.lex as lex
import sys
import os
import os.path

tokens = [
  'TERM',
  'NONTERM',
  'START',
  'EPS',
  'TO',
  'SEPARATOR'
]


t_EPS = r'eps'
t_TO = r'to'
t_SEPARATOR = r';'
t_ignore = ' \t'


def t_TERM(t):
    r't\'[ -~]+?\'t'
    t.value = t.value[2:-2]
    return t


def t_NONTERM(t):
    r'n\'[ -~]+?\'n'
    t.value = t.value[2:-2]
    return t


def t_START(t):
    r'set\_start [^;]+'
    t.value = t.value[10:]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

#input and output are files
def run_lexer(input, output):
    lexer.lineno = 1
    for line in input.readlines():
            lexer.input(line)
            cur_token = lexer.token()
            while cur_token:
                output.write(str(cur_token) + '\n')
                cur_token = lexer.token()


def run_tests():
    tests = os.listdir(os.path.join(os.getcwd(), 'examples'))
    for test in tests:
        if '.out' in test:
            continue
        input = os.path.join(os.getcwd(), 'examples', test)
        output = os.path.splitext(input)[0] + '_lex.out'
        with open(input, "r") as fin:
            with open(output, "w") as fout:
                run_lexer(fin, fout)
        

def main():
    run_tests()
    for i in range(1, len(sys.argv)):
        with open(sys.argv[i], "r") as input:
            with open(sys.argv[i] + '.out', "w") as output:
                run_lexer(input, output)
                        

if __name__ == "__main__":
    main()