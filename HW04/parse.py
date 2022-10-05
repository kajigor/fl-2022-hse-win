import ply.yacc as yacc
import sys
from lex import tokens

# token : TERM
#       | NON_TERM
#       | EPS
# tokens : token
#        | tokens token
# union : tokens
#       | union UNION tokens
# start : START
# rule : NON_TERM EQ union ENDL


class Grammar:
    terms = set()
    non_terms = set()
    rules = list()
    start = ""

    def to_string(self):
        result = "Start: " + self.start + "\n"
        result += "Terminals: " + str(self.terms) + "\n"
        result += "Non terminals: " + str(self.non_terms) + "\n"
        result += "Rules: \n"
        for rule in self.rules:
            result += "\t"
            result += rule[0] + " = "
            for i in range(len(rule[1])):
                if i > 0:
                    result += " \| "
                tokens = rule[1][i]
                result += " ".join(tokens)
            result += "\n"
        return result


grammar = Grammar()


def p_token_term(p):
    'token : TERM'
    p[0] = p[1]
    grammar.terms.add(p[0])


def p_token_non_term(p):
    'token : NON_TERM'
    p[0] = p[1]
    grammar.non_terms.add(p[0])


def p_token_eps(p):
    'token : EPS'
    p[0] = p[1]


def p_tokens_token(p):
    'tokens : token'
    p[0] = [p[1]]


def p_tokens_tokens_token(p):
    'tokens : tokens token'
    p[0] = p[1] + [p[2]]


def p_union_tokens(p):
    'union : tokens'
    p[0] = [p[1]]


def p_union_union_tokens(p):
    'union : union UNION tokens'
    p[0] = p[1] + [p[2]]


def p_rule(p):
    'rule : NON_TERM EQ union ENDL'
    p[0] = (p[1], p[3])
    grammar.rules.append(p[0])


def p_start_start(p):
    'start : START'
    p[0] = p[1]
    grammar.start = p[0]


def p_error(p):
    if p is None:
        print("Unexpected end of input")
    else:
        t = f"{p.type}({p.value}) at {p.lineno}:{p.lexpos}"
        print(f"Syntax error: Unexpected {t}", p)
    

def main():
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])

        with open(filename, 'r') as fin, open(filename + ".out", "w") as fout:
            parser = yacc.yacc()
            parser.parse("".join(fin.readlines()))

            print(grammar.to_string(), file=fout)


if __name__ == "__main__":
    main()
