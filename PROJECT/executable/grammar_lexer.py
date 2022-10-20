import ply.lex as lex
import sys
import re

error = False
f_outp = None

reserved = {
    'S': 'START_NON_TERM',
    'E': 'EPSILON'
}

tokens = [
             'TERM',
             'NON_TERM',
             'EQ',
             'END'
         ] + list(reserved.values())


def t_TERM(t):
    r"(?<!\\)\'.+?((?<!\\)|(?<=\\\\))\'"
    t.value = (t.value[1:-1])
    t.type = reserved.get(t.value, 'TERM')
    t.value = re.sub(r"\\(.)", r"\1", t.value) # здесь в t.value записывается строка без экранирований
    return t

def t_NON_TERM(t):
    r"(?<!\\)<.+?((?<!\\)|(?<=\\\\))>"
    t.value = (t.value[1:-1])
    t.type = reserved.get(t.value, 'NON_TERM')
    t.value = re.sub(r"\\(.)", r"\1", t.value)
    return t


t_EQ = r'='
t_END = r';'

t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    global f_outp
    global error
    print("Illegal character '%s'" % t.value[0], file=f_outp)
    error = True
    t.lexer.skip(len(t.value))


lexer = lex.lex()


def main():
    global f_outp
    global error
    lexer = lex.lex()
    f_outp = open(sys.argv[1] + ".out", "w")

    with open(sys.argv[1], "r") as f_inp:
        for line in f_inp:
            lexer.input(line)
            tokens = []
            while True:
                tok = lexer.token()
                if not tok or error:
                    break
                else:
                    tokens.append(tok)
            if not error:
                for tok in tokens:
                    print(tok, file=f_outp)
            else:
                error = False


if __name__ == "__main__":
    main()
