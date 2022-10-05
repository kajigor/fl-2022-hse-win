import ply.lex as lex
import sys

def remove_slash(t):
  return t.replace("//", "/").replace("/(", "(").replace("/)", ")").replace("/[", "[").replace("/]", "]")

tokens = [
    'BEGIN',
    'TERMINAL',
    'NONTERMINAL',
    'ASSIGNMENT',
    'SEPARATE',
    'END'
]

t_SEPARATE = r';'
t_ASSIGNMENT = r'->'
t_END = r'end'

t_ignore = ' \t'

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

def t_BEGIN(t):
  r'begin=(.+);'
  t.value = remove_slash(t.value[7:-2])
  return t

def t_TERMINAL(t):
  r'\[((.*?[^\/])|)\]'
  t.value = remove_slash(t.value[1:-1])
  return t

def t_NONTERMINAL(t):
  r'\(((.*?[^\/])|)\)'
  t.value = remove_slash(t.value[1:-1])
  return t



lexer = lex.lex()
def main():
  lexer = lex.lex()
  rfile = open(sys.argv[1])
  input = rfile.read()
  lexer.input(input)
  wfile = open(sys.argv[1] + ".out", 'w')
  while True:
    tok = lexer.token()
    if not tok:
      break
    wfile.write(str(tok) + '\n')

if __name__ == "__main__":
    main()