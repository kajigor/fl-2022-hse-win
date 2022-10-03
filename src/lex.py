import ply.lex as lex
import sys
import re
import os

tokens = [
  'TERMS',
  'NONTERMS',
  'START',
  'TO',
  'EPS',
  'SEPARATOR'
]

t_TO = '->'
t_EPS = 'eps'
t_SEPARATOR = ';'

def t_TERMS(t):
  r'terminals{.+?(?<!(?<!\\)\\)}'
  t.value = re.split(r'(?<!(?<!\\)\\),\s*', t.value[10:-1])
  return t


def t_NONTERMS(t):
  r'nonterminals{.+?(?<!(?<!\\)\\)}'
  t.value = re.split(r'(?<!(?<!\\)\\),\s*', t.value[13:-1])
  return t


def t_START(t):
  r'start{.+?(?<!(?<!\\)\\)}'
  t.value = t.value[6:-1]
  return t



t_ignore = ' \t'

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

lexer = lex.lex()

# no sh script.
def run_lex_tests():
  from pathlib import Path
  dir = os.getcwd() + '/tests'
  print(os.listdir(dir))
  for file in os.listdir(dir):
    with open(dir + '/' + file, 'r') as fin, open(os.getcwd() + '/lexer_tests_out/' + file + '.out', 'w') as fout:
      text = fin.read()
      lexer = lex.lex()

      lexer.input(text)
      token = lexer.token()
    
      while token:
        fout.write(str(token) + '\n')
        token = lexer.token()

def main():
  if sys.argv[1] == '--test':
    run_lex_tests()
  else:
    with open(sys.argv[1], 'r') as fin, open(sys.argv[1] + '.out', 'w') as fout:

      lexer = lex.lex()
      text = fin.read()
      lexer.input(text)

      token = lexer.token()
    
      while token:
        fout.write(token)
        token = lexer.token()

if __name__ == "__main__":
    main()