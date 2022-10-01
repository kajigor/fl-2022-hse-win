import ply.yacc as yacc
import sys

from lex import tokens

# SINGLE_TOKEN    : TERM
#                 | NTERM
#                 | EPSILON
#                 | STARTTERM
# MULTIPLE_TOKENS : SINGLE_TOKEN
#                 | MULTIPLE_TOKENS SINGLE_TOKEN
# RULE            : NTERM ARROW MULTIPLE_TOKENS SEPARATOR
#                 | STARTTERM ARROW MULTIPLE_TOKENS SEPARATOR

class Grammar:
    terminals = set()
    not_terminals = set()
    start = ""
    rules = []

    def clear(self):
        self.terminals = set()
        self.not_terminals = set()
        self.rules = []
        self.start = ''

    def __str__(self):
        res  = "Terminals:\n"
        self.terminals = sorted(list(self.terminals))
        for terminal in self.terminals:
            res += "\t" + terminal + "\n"

        res += "Non terminals:\n"
        self.not_terminals = sorted(list(self.not_terminals))
        for not_terminal in self.not_terminals:
            res += "\t" + not_terminal + "\n"

        res += "Starting non terminal: " + self.start + "\n"

        dict_help = {}
        for rule in self.rules:
            cur = ''
            for x in rule[1]:
                cur += x
            if rule[0] in dict_help.keys():
                dict_help[rule[0]].append(cur)
            else:
                dict_help[rule[0]]= [cur]

        res += "Rules:\n"
        for rule_begin in sorted(dict_help.keys()):
            res += '\t'
            res += rule_begin + " → "
            for x in dict_help[rule_begin]:
                res += x + " | "
            res = res[:-3]
            res += '\n'

        return res

grammar = Grammar()

def p_rule_nterm(p):
    "RULE : NTERM ARROW MULTIPLE_TOKENS SEPARATOR"
    grammar.not_terminals.add(p[1])
    p[0] = (p[1], p[3])
    grammar.rules.append(p[0])

def p_rule_startterm(p):
    "RULE : STARTTERM ARROW MULTIPLE_TOKENS SEPARATOR"
    grammar.start = p[1]
    grammar.not_terminals.add(p[1])
    p[0] = (p[1], p[3])
    grammar.rules.append((p[1], p[3]))

def p_single_token_term(p):
    'SINGLE_TOKEN : TERM'
    p[0] = p[1]
    grammar.terminals.add(p[0])

def p_single_token_nterm(p):
    'SINGLE_TOKEN : NTERM'
    p[0] = p[1]
    grammar.not_terminals.add(p[0])

def p_single_token_start_term(p):
    'SINGLE_TOKEN : STARTTERM'
    p[0] = p[1]
    grammar.start = p[0]
    grammar.not_terminals.add(p[0])

def p_single_token_eps(p):
    'SINGLE_TOKEN : EPSILON'
    p[0] = p[1]

def p_multiple_tokens_single(p):
    'MULTIPLE_TOKENS : SINGLE_TOKEN'
    p[0] = [p[1]]

def p_multiple_tokens_many(p):
    'MULTIPLE_TOKENS : MULTIPLE_TOKENS SINGLE_TOKEN'
    p[0] = p[1] + [p[2]]

def p_error(p):
    if p is None:
        print("Unexpected EOF")
    else:
        print(f"Syntax error: Unexpected {p.type}({p.value}) on line {p.lineno}")
    exit(123)

def test(parser):
    tests = ["arithmetic", "brackets", "palindromes"]
    for cur_test in tests:
        with open("tests_and_examples/" + cur_test + ".txt", "r") as f:
            with open("tests_and_examples/" + cur_test + ".pars.ans", "r") as f1:
                for line in f.readlines():
                    parser.parse(line)
                lines = f1.readlines()
                lines1 = str(grammar).split('\n')[:-1]
                assert len(lines) == len(lines1)
                for i in range(len(lines)):
                    assert lines[i] == lines1[i] + '\n'
                grammar.clear()

def main():
    parser = yacc.yacc()

    test(parser)

    with open(sys.argv[1], "r") as f:
        with open(sys.argv[1] + ".out", "w") as f1:
            for line in f.readlines():
                parser.parse(line)
            f1.write(str(grammar))
            grammar.clear()

if __name__ == "__main__":
    main()
