import ply.yacc as yacc
import sys

from typing import Set

from lex import tokens


class Terminal:
    data: str


class NonTerminal:
    data: str


class Start:
    data: str


class Empty:
    data: str


class Grammar:
    data: [Set[Terminal], Set[NonTerminal], Start, Empty]


def p_initial(p):
    'initial : start'
    Start.data = p[1]


def p_empty(p):
    'empty :'
    pass


def p_terminal(p):
    pass


def p_error(p):
    if p == None:
        token = "end of file"
        p.error()
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 <run_file> <input_file>")
        return

    input_file = str(sys.argv[1])
    output_file = input_file + ".out"

    with open(input_file, "r") as input, open(output_file, "w") as output:
        parser = yacc.yacc(start="initial")
        result = parser.parse("".join(input.readlines()))
        print(result, file=output)


if __name__ == "__main__":
    main()

# def p_expr_plus(p):
#   'expr : expr PLUS term'
#   p[0] = p[1] + p[3]

# def p_expr_minus(p):
#   'expr : expr MINUS term'
#   p[0] = p[1] - p[3]

# def p_expr_term(p):
#   'expr : term'
#   p[0] = p[1]

# def p_term_mult(p):
#   'term : term MULT factor'
#   p[0] = p[1] * p[3]

# def p_term_div(p):
#   'term : term DIV factor'
#   p[0] = p[1] / p[3]

# def p_term_factor(p):
#   'term : factor'
#   p[0] = p[1]

# def p_factor_num(p):
#   'factor : NUM'
#   p[0] = p[1]

# def p_factor_br(p):
#   'factor : LBR expr RBR'
#   p[0] = p[2]
