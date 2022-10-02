import ply.lex as lex
import sys

reserved = {
  "start" : "START",
  "eps" : "EPS"
}

tokens = [
  'TERM',
  'NONTERM',
  'KEYWORD',
  'OR',
  'ARROW',
  'LINEBREAK'
] + list(reserved.values())

def t_TERM(t):
  r'\[[\x00-\x7F]+?\]'
  t.value = t.value[1:-1]
  return t

def t_NONTERM(t):
  r'\([\x00-\x7F]+?\)'
  t.value = t.value[1:-1]
  return t
  
def t_KEYWORD(t):
  r'[A-Za-z]+'
  if t.value not in reserved:
    print(f"Illegal sequence: {t.value}")
    return
  t.type = reserved[t.value]
  return t

t_ARROW = r'\-\>'
t_OR = r'\|'
t_LINEBREAK = r'\;'
t_ignore = ' \t'

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)
  

lexer = lex.lex()

def main():
  result = ""
  filename = sys.argv[1]

  try:
    file = open(filename)
  except:
    pass

  text = file.read()
  lexer.input(text)
  while True:
    tok = lexer.token()
    if not tok:
      break
    result += str(tok) + "\n"
  with open(filename + ".out", "w") as fo:
    fo.write(result)

if __name__ == "__main__":
  main()