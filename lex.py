import ply.lex as lex
import sys

reserved = {
    'start': 'START',
}

tokens = [
             'TERM',
             'NTERM',
             'EPSILON',
             'BIND',
             'OR',
             'END_OF_RULE'
         ] + list(reserved.values())

t_ignore = r' \t'
t_OR = r'\|'
t_BIND = r'='
t_EPSILON = r'\#eps\#'
t_END_OF_RULE = r';'

error = False


def clean(t):
    return t.replace("\\\$", "\$").replace("\\\\", "\\")


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    global error
    print("Illegal character {0} at position {1} at line {2}".format(t.value[0], t.lexer.lexpos, t.lexer.lineno))
    print("Cannot proceed analysis, exiting...")
    error = True
    t.lexer.skip(1)


def t_TERM(t):
    r'\$[^$\\]+((\\\$)?[^$\\]*)*\$'
    t.value = clean(t.value[:])
    return t


def t_NTERM(t):
    r'\#[^#\\]+((\\\#)?[^#\\]*)*\#'
    t.value = clean(t.value[:])
    return t


def main():
    if len(sys.argv) > 1:
        file = sys.argv[1]

        with open(file, 'r') as inf, open(file + ".out", 'w') as outf:
            lexer = lex.lex()
            lex_input = "".join(inf.readlines())
            lexer.input(lex_input)

            while True:
                tok = lexer.token()
                if not tok or error:
                    break
                print(tok, file=outf)


if __name__ == "__main__":
    main()
