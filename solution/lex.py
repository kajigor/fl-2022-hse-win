import ply.lex as lex
import sys

tokens = [
    'TERMINAL',
    'NON_TERMINAL',
    'START',
    'ARROW',
    'EPSILON',
    'SEPARATOR',
    'OR'
]

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
  print(f"Illegal character: {t.value[0]}")
  t.lexer.skip(1)

t_ignore = ' \t'
t_ARROW = r'->'
t_EPSILON = r'e'
t_SEPARATOR = r';'
t_OR = r'\|'

def t_TERMINAL(t):
    r'\'(([^\\])|(\\[\x00-\x7F]))*?\''
    t.value = t.value[1:-1].replace("\\'", "'").replace("\\\\", "\\")
    return t

def t_NON_TERMINAL(t):
    r'\$(([^\\])|(\\[\x00-\x7F]))*?\$'
    t.value = t.value[1:-1].replace("\\$", "$").replace("\\\\", "\\")
    return t

def t_START(t):
    r'start->\$(([^\\])|(\\[\x00-\x7F]))*?\$'
    t.value = t.value[8:-1].replace("\\$", "$").replace("\\\\", "\\")
    return t

lexer = lex.lex()

def main():
    input_file = sys.argv[1]
    output_file = input_file + ".out"
    with open(input_file, "r") as file1:
        with open(output_file, "w") as file2:
            for data in file1:
                lexer.input(data)
                while True:
                    tok = lexer.token()
                    if not tok:
                        break
                    file2.write(str(tok) + '\n')


if __name__ == "__main__":
    main()
