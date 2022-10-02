import ply.yacc as yacc
import sys

from dataclasses import dataclass
from typing import List, Set
from lexer import tokens


# lexical rules:
#
# elem : non_terminal
#      | terminal
#      | eps
#
# term : elem
#      | term elem
#
# expr : term
#      | expr next_term term
#
# bind : non_terminal equiv expr

@dataclass
class Nan:
    pass


@dataclass
class Element:
    pass


@dataclass
class NonTerminal(Element):
    name: str


@dataclass
class Terminal(Element):
    value: str


@dataclass
class Eps(Element):
    pass


def show_elem(elem):
    if isinstance(elem, Eps):
        return "eps"
    elif isinstance(elem, NonTerminal):
        return f'/{elem.name}/'
    elif isinstance(elem, Terminal):
        return f'"{elem.value}"'
    else:
        print(type(elem))
        raise ValueError("Element is not valid")


@dataclass
class Term:
    elements: List[Element]


def make_term(lhs, rhs):
    if isinstance(lhs, Term):
        if isinstance(rhs, Nan):
            return lhs
        if isinstance(rhs, Term):
            return Term(lhs.elements + rhs.elements)
        return Term(lhs.elements + [rhs])
    if isinstance(rhs, Nan):
        return Term([lhs])
    return Term([lhs, rhs])


@dataclass
class Expr:
    terms: List[Term]


def make_expr(lhs, rhs):
    if isinstance(lhs, Expr):
        if isinstance(rhs, Nan):
            return lhs
        if isinstance(rhs, Expr):
            return Expr(lhs.terms + rhs.terms)
        return Expr(lhs.terms + [make_term(rhs, Nan())])
    if isinstance(rhs, Nan):
        return Expr([make_term(lhs, Nan())])
    return Expr([make_term(lhs, Nan()), make_term(rhs, Nan())])


def show_expr(expr):
    result = ""
    for term in expr.terms:
        result += "".join((map(show_elem, term.elements))) + " | "
    return result[:-3]


@dataclass
class Rule:
    n_term: str
    expr: Expr


def show_rule(grammar, curr_n_term):
    curr_rule_expr = Expr([])
    for rule in grammar.rules:
        if rule.n_term == curr_n_term:
            curr_rule_expr = make_expr(curr_rule_expr, rule.expr)
    if len(curr_rule_expr.terms):
        return curr_n_term + " = " + show_expr(curr_rule_expr) + ";\n"
    return ""


@dataclass
class Grammar:
    terminals: Set[str]
    non_terminals: Set[str]
    start: str
    rules: List[Rule]


def find_terminals(expr):
    result = set()
    for term in expr.terms:
        for elem in term.elements:
            if isinstance(elem, Terminal):
                result = result.union({elem.value})
    return result


def find_non_terminals(expr):
    result = set()
    for term in expr.terms:
        for elem in term.elements:
            if isinstance(elem, NonTerminal):
                result = result.union({elem.name})
    return result


def make_grammar(start, rules):
    terminals = find_terminals(rules[0].expr)
    for i in rules[1:]:
        terminals = terminals.union(find_terminals(i.expr))

    non_terminals = {start}
    for i in rules:
        non_terminals = non_terminals.union(find_non_terminals(i.expr)).union({i.n_term})

    return Grammar(terminals, non_terminals, start, rules)


def show_grammar(grammar):
    result = "Context Free Grammar: Syntactic analysis completed\n"
    result += f"List of terminal characters: {grammar.terminals}\n"
    result += f"List of non-terminal characters: {grammar.non_terminals}\n"
    result += f"Start non-terminal character: {grammar.start}\n"
    result += "Rules:\n"
    for grammar_n_term in grammar.non_terminals:
        result += show_rule(grammar, grammar_n_term)
    return result


def p_grammar(p):
    'grammar : START rules'
    p[0] = make_grammar(p[1], p[2])


def p_rules(p):
    '''rules : rule
             | rules rule'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_rule(p):
    'rule : NON_TERMINAL EQUIV expr END_OF_LINE'
    p[0] = Rule(p[1], p[3])


def p_expr(p):
    '''expr : expr NEXT_TERM term
            | term'''
    if len(p) == 4:
        p[0] = make_expr(p[1], p[3])
    else:
        p[0] = make_expr(p[1], Nan())


def p_term(p):
    '''term : elem
            | term elem'''
    if len(p) == 3:
        p[0] = make_term(p[1], p[2])
    else:
        p[0] = make_term(p[1], Nan())


def p_elem_terminal(p):
    'elem : TERMINAL'
    p[0] = Terminal(p[1])


def p_elem_non_terminal(p):
    'elem : NON_TERMINAL'
    p[0] = NonTerminal(p[1])


def p_elem_eps(p):
    'elem : EPS'
    p[0] = Eps()


def p_error(p):
    if p is None:
        print("Unexpected end of input")
    else:
        token = f"{p.type}({p.value}) at {p.lineno}:{p.lexpos}"
        print(f"Syntax error: Unexpected {token}")
    exit()


parser = yacc.yacc()


def main():
    filename = sys.argv[1]
    with open(filename, "r") as filein, open(filename + ".out", "w") as fileout:
        print(show_grammar(parser.parse("".join(filein.readlines()))), file=fileout, end='')


if __name__ == "__main__":
    main()
