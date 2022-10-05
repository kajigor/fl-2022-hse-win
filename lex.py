import ply.lex as lex
import sys

tokens = [
             'TERM',
             'NTERM',
             'EPSILON',
             'BIND',
             'OR',
             'END_OF_RULE',
             'SEP'
         ]

t_ignore = ' \t'
t_OR = r'\|'
t_BIND = r'='
t_EPSILON = r'eps'
t_END_OF_RULE = r';'
t_SEP = r'&'


def clean(t):
    return t.replace("\\\$", "\$").replace("\\\\", "\\")


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



def t_error(t):
    global error
    print("Illegal character {0} at position {1} at line {2}".format(t.value[0], t.lexer.lexpos, t.lexer.lineno))
    print("Cannot proceed analysis, exiting...")
    exit()


def t_NTERM(t):
    r'\$[^$\\]+((\\\$)?[^$\\]*)*\$'
    t.value = clean(t.value[:])
    return t


def t_TERM(t):
    r'\#[^#\\]+((\\\#)?[^#\\]*)*\#'
    t.value = clean(t.value[:])
    return t

lexer = lex.lex()

def main():
    if len(sys.argv) > 1:
        file = sys.argv[1]

        with open(file, 'r') as inf, open(file + ".out", 'w') as outf:
            lex_input = "".join(inf.readlines())
            lexer.input(lex_input)

            while True:
                tok = lexer.token()
                if not tok:
                    break
                print(tok, file=outf)


if __name__ == "__main__":
    main()
