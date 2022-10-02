import ply.lex as lex
import sys

tokens = [
  'START',
  'ARROW',
  'SEPARATOR',
  'END',
  'EMPTY',
  'NON_TERMINAL',
  'TERMINAL',
]

t_ignore = ' \t'

def t_newline(token):
  r'\n+'
  token.lexer.lineno += len(token.value)

def t_error(token):
  print("Illegal character '%s'" % token.value[0])
  token.lexer.skip(1)

def t_START(token):
  r'start=🤯[\x00-\x7F]+🤯'
  token.value = token.value[7:-1]
  return token

t_ARROW = r'->'

t_SEPARATOR = r'\|'

t_END = r'🗿'

t_EMPTY = r'😵'

def t_NON_TERMINAL(token):
  r'🤯[\x00-\x7F]+🤯'
  token.value = token.value[1:-1]
  return token

def t_TERMINAL(token):
  r'🥵[\x00-\x7F]+🥵'
  token.value = token.value[1:-1]
  return token

lexer = lex.lex()

def main():
  lexer = lex.lex()

  if len(sys.argv) > 1:
    filename = sys.argv[1]

    with open(filename, "r", encoding="utf-8") as grammar, open(filename + ".out", "w", encoding="utf-8") as output_grammar:
      lexer.input("".join(grammar.readlines()))

      while token := lexer.token():
        print(token, file=output_grammar)
  else:
    while True:
      lexer.input(input("> "))

      while token := lexer.token():
        print(token)


if __name__ == "__main__":
  main()