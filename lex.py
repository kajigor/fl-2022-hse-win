import ply.lex as lex
import sys

reserved = {
  'to': 'RULER'
}

tokens = [
  'TERM',
  'NONTERM',
  'START',
  'EPS'
] + list(reserved.values())


def t_TERM(t):
    r't\'[ -~]+\'t'
    t.value = t.value[2:-2]
    return t


def t_NONTERM(t):
    r'n\'[ -~]+\'n'
    t.value = t.value[2:-2]
    return t


def t_START(t):
    r'set\_start [ -~]+'
    t.value = t.value[11:]
    return t


t_EPS = r'eps'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def run_tests():
    


def main():
    run_tests()

    input_count = len(sys.argv)
    for i in range(1, len):
        with open(sys.argv[i], "r") as input:
            with open(sys.argv[i], "w") as output:
                for line in input.readlines():
                    lexer.input(line)
                    cur_token = lexer.token()
                    while cur_token:
                        print(cur_token, end = '\n')
                        cur_token = lexer.token()

if __name__ == "__main__":
    main()