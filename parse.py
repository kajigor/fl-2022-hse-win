import sys

import ply.yacc as yacc

from lex import tokens


class ContextFreeGrammar:
    terms = set()
    non_terms = set()
    rules = {}
    start = ''

    def set_start(self, st):
        if self.start != "":
            print("Error: multiple start non-terminals!")
        self.start = st

    def __str__(self):
        res = "Start non-terminal:\n\t" + self.start + '\n'
        res += "Non-terminals:\n\t" + "\n\t".join(self.non_terms) + '\n'
        res += "Terminals:\n\t" + "\n\t".join(self.terms) + '\n'
        res += "Rules:\n\t" + "\n\t".join(
                [l + '->' + ' | '.join([''.join(i) for i in r]) for l, r in self.rules])

    def clear(self):
        self.terms.clear()
        self.rules.clear()
        self.non_terms.clear()
        self.start = ''


grammar = ContextFreeGrammar()


# grammar : rule SEP grammar | rule
# rule : rule_left RULE tokens
# rule_left : START NON_TERM | NON_TERM
# tokens : token tokens | token
# token : NON_TERM | TERM


def p_grammar(p):
    '''
        grammar : rule SEP grammar
                | rule
    '''
    if len(p) == 4:
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]


def p_rule(p):
    'rule : rule_left RULE tokens'
    grammar.rules[p[1]] = grammar.rules.get(p[1], []) + [p[4]]


def p_rule_left(p):
    '''
        rule_left : START NON_TERM
                  | NON_TERM
    '''
    if len(p) == 3:
        grammar.set_start(p[2])
    p[0] = p[-1]


def p_tokens(p):
    '''
        tokens : token tokens
               | token
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


def p_token_term(p):
    'token : TERM'
    p[0] = p[1]
    grammar.terms.add(p[0])


def p_token_non_term(p):
    'token : NON_TERM'
    p[0] = p[1]
    grammar.non_terms.add(p[0])


def p_error(p):
    if p == None:
        token = "end of file"
        parser.errok()
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")


parser = yacc.yacc()


def main():
    parser.parse(open(sys.argv[1], mode='r').read())
    open(sys.argv[1] + '.out', mode='w').write(str(grammar))


if __name__ == "__main__":
    main()
