import ply.yacc as yacc

from lex import tokens
import sys
import os
import os.path

# token : TERM
#       | NONTERM
#       | EPS
# mult_tokens : token
#             | mult_tokens token
# expr : START SEPARATOR
#      | rule SEPARATOR 
# rule : mult_tokens TO mult_tokens

class Grammar:
    terminals = set()
    nonterminals = set()
    rules = set()
    start = ""
    
    def clear(self):
        self.terminals.clear()
        self.nonterminals.clear()
        self.rules.clear()
        self.start = ""

    def get(self):
        res = ""
        res += "Start: \n"
        res += self.start + '\n'
        res += "NonTerminals: \n"
        for nonterm in self.nonterminals:
            res += nonterm + '\n'
        res += "Terminals: \n"
        for term in self.terminals:
            res += term + '\n'
        res += "Rules: \n"
        for rule in self.rules:
            res += str(rule[0]) + " to " + str(rule[1])
        return res


grammar = Grammar()

def p_token_term(p):
    'token : TERM'
    p[0] = p[1]
    grammar.terminals.add(p[0])


def p_token_NONTERM(p):
    'token : NONTERM'
    p[0] = p[1]
    grammar.nonterminals.add(p[0])


def p_token_eps(p):
    'token : EPS'
    p[0] = p[1]


def p_token_start(p):
    'token : START SEPARATOR'
    p[0] = p[1]
    if grammar.start != "":
        print("error: ambiguous start")
    grammar.start = p[0]


def p_mtokens_token(p):
    'mult_tokens : token'
    p[0] = list(p[1])


def p_mtokens_mtokens_token(p):
    'mult_tokens : mult_tokens token'
    p[0] = p[1] + list(p[2])


def p_expr_start(p):
    'expr : START SEPARATOR'
    p[0] = p[1]
    print(1)


def p_expr_rule(p):
    'expr : rule SEPARATOR'
    p[0] = p[1]
    print(1)


def p_rule(p):
    'rule : mult_tokens TO mult_tokens'
    p[0] = (p[1], p[3])
    grammar.rules.add(p[0])

def p_error(p):
  if p == None:
    print("Unexpected EOF")
  else:
    token = f"{p.type}({p.value}) on line {p.lineno}"

  print(f"Syntax error: Unexpected {token}")

parser = yacc.yacc()

def run_parser(input, output):
    for line in input.readlines():
        parser.parse(line)
    output.write(grammar.get())
    grammar.clear()

def run_tests():
    tests = os.listdir(os.path.join(os.getcwd(), 'examples'))
    for test in tests:
        if '.out' in test:
            continue
        input = os.path.join(os.getcwd(), 'examples', test)
        output = os.path.splitext(input)[0] + '_parse.out'
        with open(input, "r") as fin:
            with open(output, "w") as fout:
                run_parser(fin, fout)
        

def main():
    run_tests()
    for i in range(1, len(sys.argv)):
        with open(sys.argv[i], "r") as input:
            with open(sys.argv[i] + '.out', "w") as output:
                run_parser(input, output)

if __name__ == "__main__":
    main()
