import ply.yacc as yacc
import sys
import os

from pprint import pprint
from lex import tokens

class Grammar:
  def __init__(self):
    self.start = ''
    self.terminals = set([])
    self.nonterminals = set([])
    self.rules = []
    self.cnf = True

  def print_(self):
    print('Start terminal is:', self.start)
    print('Terminals are:')
    pprint(self.terminals)
    print('Nonterminals are:')
    pprint(self.nonterminals)
    print('Rules are:')
    pprint(self.rules)
    print('Chomsky normal form:', self.cnf)

  def print_p(self):
    print('Start terminal is:', self.start)
    print('\nTerminals are:')
    print (*self.terminals, sep = ', ')
    print('\nNonterminals are:')
    print (*self.nonterminals, sep = ', ')
    print('\nRules are:')
    for i in range(len(self.rules)):
        print(self.rules[i][0][0], '->', ''.join(self.rules[i][1]))
    if (self.cnf):
      print('\nGrammar is in Chomsky normal form')
    else:
      print('\nGrammar is not in Chomsky normal form')

  def check_cnf(self):
    for rule in self.rules:
      if len(rule[1]) > 2:
        return False
      if len(rule[1]) == 2:
        if not (rule[1][0] in self.nonterminals and rule[1][0] in self.nonterminals):
          return False
      if rule[1][0] == 'eps' and rule[0][0] != self.start:
        return False
      if rule[1][0] != 'eps' and not rule[1][0] in self.terminals:
        return False
      
      return True
#class Grammar

grammar = Grammar()

def p_build(p):
  'build : START SEPARATOR rules'
  grammar.start = p[1]
  grammar.rules = p[3]
  grammar.nonterminals.add(p[1])

def p_rules(p):
  '''rules : rule
           | rules rule'''
  
  if (len(p) > 2):
    p[0] = p[1] + [p[2]]
  else: 
    p[0] = [p[1]]

def p_rule(p):
  'rule : NONTERMS TO expr SEPARATOR'
  
  grammar.nonterminals.update(p[1])
  p[0] = (p[1], p[3])

def p_expr(p):
  '''expr : single
          | expr single'''
  
  if (len(p) > 2):
    p[0] = p[1] + p[2]
  else :
    p[0] = p[1]

def p_single(p):
  '''single : term
            | nonterm
            | EPS'''
  if (p[1] == 'eps'):
    p[0] = [p[1]]
  else :
    p[0] = p[1]

def p_term(p):
  'term : TERMS'
  p[0] = p[1]
  grammar.terminals.update(p[1])

def p_nonterm(p):
  'nonterm : NONTERMS'
  p[0] = p[1]
  grammar.nonterminals.update(p[1])

def p_error(p):
  if (p is None) :
    print ('Expected token, but EOF found')
  else :
    print ('Error: invalid syntax', p)
  exit()

def run_parser_tests():
  from pathlib import Path
  dir = os.getcwd() + '/tests'
  print(os.listdir(dir))
  for file in os.listdir(dir):
    with open(dir + '/' + file, 'r') as fin, open(os.getcwd() + '/parser_tests_out/' + file + '.out', 'w') as fout:
      text = fin.read()
      parser = yacc.yacc()

      parser.parse(text)

      grammar.cnf = grammar.check_cnf()
      
      origin = sys.stdout
      sys.stdout = fout

      grammar.print_()
      print('\n\n ***  Pretty output  *** \n\n')
      grammar.print_p()

      sys.stdout = origin


def main():
  parser = yacc.yacc()

  if sys.argv[1] == '--test':
    run_parser_tests()

  else:
    with open(sys.argv[1], 'r') as fin, open(sys.argv[1] + '.out', 'w') as fout:

      text = fin.read()
      parser.parse(text)
      grammar.cnf = grammar.check_cnf()
      
      origin = sys.stdout
      sys.stdout = fout

      grammar.print_()
      print('\n\n ***  Pretty output  *** \n\n')
      grammar.print_p()

      sys.stdout = origin

if __name__ == "__main__":
    main()

