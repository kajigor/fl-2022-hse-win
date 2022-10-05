import ply.yacc as yacc
import sys

from lexer import tokens


# start : BEGIN | END | rule
# rule : NONTERMINAL ASSIGNMENT multiple
# single : TERMINAL | NONTERMINAL
# multiple : multiple single | single
# end : END

class Grammar:
    start = ""
    terminals = set()
    nonterminals = set()
    rules = set()

    def print(self):
        out = "Grammar" + "\n"
        out += "Start non-terminal: " + self.start + "\n"
        out += "Terminals: " + ', '.join(self.terminals) + "\n"
        out += "Non-terminals: " + ', '.join(self.nonterminals) + "\n"
        out += "Rules: " + ', '.join(self.rules) + "\n"
        if self.is_Chomsky_normal_form() :
            out += "grammar is in Chomsky normal form" + "\n"
        else:
            out += "grammar is not in Chomsky normal form" + "\n"
        return out

    def is_Chomsky_normal_form(self):
        for rule in self.rules:
            start = rule.find("->") + 2
            if (rule[start:] == "") and (rule[:start-2] == start):
                continue
            elif rule[start:] in self.terminals:
                continue
            else:
                flag = False
                for i in range(start, len(rule)):
                    if (rule[start:i] in self.nonterminals) and (rule[i:] in self.nonterminals):
                        flag = True
                        break
                if flag:
                    continue
            return False
        return True


grammar = Grammar()


def p_error(p):
    if p == None:
        print("end of file")
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"
    print(f"Syntax error: Unexpected {token}")


def p_begin(p):
    'start : BEGIN'
    p[0] = p[1]
    grammar.start = p[0]


def p_begin_rule(p):
    'start : rule'
    p[0] = p[1]


def p_end(p):
    'start : END'
    p[0] = p[1]


def p_rule(p):
    'rule : NONTERMINAL ASSIGNMENT multiple SEPARATE'
    p[0] = p[1] + "->" + ''.join(p[3])
    grammar.rules.add((p[0]))


def p_multiple_single(p):
    'multiple : single'
    p[0] = list(p[1])


def p_really_multiple(p):
    'multiple : multiple single'
    p[0] = p[1] + list(p[2])


def p_nonterminal(p):
    'single : NONTERMINAL'
    p[0] = p[1]
    grammar.nonterminals.add(p[0])


def p_terminal(p):
    'single : TERMINAL'
    p[0] = p[1]
    grammar.terminals.add(p[0])


def main():
    parser = yacc.yacc()
    rfile = open(sys.argv[1])
    wfile = open(sys.argv[1] + ".out", 'w')
    for line in rfile.readlines():
        parser.parse(line)
    wfile.write(grammar.print())


if __name__ == "__main__":
    main()
