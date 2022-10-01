import ply.lex as lex
import sys


def escape(name : str) -> str:
  return name.replace("\\>", ">").replace("\\\\", "\\")
  

tokens = [
  'TERMINAL',
  'NON_TERMINAL',
  'BINDING',
  'ALT',
  'EPS',
  'START',
  'SEP'
]

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t):
  print(f"Unexpected character '{t.value[0]}' at line {t.lexer.lineno}")
  t.lexer.skip(1)
  

t_ALT = r'\|'
t_BINDING = r':='
t_EPS = r'EPS'
t_SEP = r';'
t_ignore = " \t"

def t_TERMINAL(t):
    r'`.+?(?<!\\)`'
    t.value = escape(t.value[1:-1])
    return t


def t_NON_TERMINAL(t):
    r'<.+?(?<!(?<!\\)\\)>'
    t.value = escape(t.value[1:-1])
    return t

def t_START(t):
    r'start=<.+?(?<!(?<!\\)\\)>'
    t.value = escape(t.value[7:-1])
    return t

lexer = lex.lex()

def main():
    if(len(sys.argv) > 1):
        filename : str = sys.argv[1]


        with open(filename, 'r') as code, open(filename + ".out", "w") as result:
            lexer = lex.lex()
            lexer.input("".join(code.readlines()))

            while token := lexer.token():
                print(token, file = result)
    else:
      while True:
        lexer = lex.lex()
        lexer.input(input())
        
        while token := lexer.token():
          print(token)

if __name__ == "__main__":
    main()
