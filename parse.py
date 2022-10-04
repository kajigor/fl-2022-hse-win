import ply.yacc as yacc
import sys
from lex import tokens
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
    rules = list()
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
            for term in rule[0]:
                res += str(term)
            res += " to "
            for term in rule[1]:
                res += str(term)
            res += '\n'
        if self.check_normal():
            res += 'grammar in Chomsky normal form'
        else:
            res += 'grammar not in Chomsky normal form'
        return res
    

    def check_normal(self):
        for rule in self.rules:
            if len(rule[0]) > 1:
                return False
            if rule[0][0] not in self.nonterminals:
                return False
            if len(rule[1]) > 2:
                return False
            if len(rule[1]) == 1 and rule[1][0] != 'eps' and rule[1][0] not in self.terminals:
                return False
            elif len(rule[1]) == 2 and (rule[1][0] not in self.nonterminals or rule[1][1] not in self.nonterminals):
                return False
        return True

grammar = Grammar()


def p_expr_start(p):
    'expr : START SEPARATOR'
    p[0] = p[1]
    if grammar.start != "":
        print("error: ambigous start")
    grammar.start = p[0]


def p_expr_rule(p):
    'expr : rule SEPARATOR'
    p[0] = p[1]


def p_rule(p):
    'rule : mult_tokens TO mult_tokens'
    p[0] = (p[1], p[3])
    grammar.rules.append(p[0])

def p_mtokens_token(p):
    'mult_tokens : token'
    p[0] = [p[1]]


def p_mtokens_mtokens_token(p):
    'mult_tokens : mult_tokens token'
    p[0] = p[1] + [p[2]]

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

def p_error(p):
  if p == None:
    token = "end of file"
    parser.errok()
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
