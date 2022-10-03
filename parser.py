# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring, invalid-name, missing-module-docstring, consider-using-f-string
import sys
from dataclasses import dataclass
from typing import List, Set, Union
from functools import reduce

import ply.yacc as yacc

from lexer import tokens


# Entity      : TERMINAL
#             | NON_TERMINAL
#             | NULL

# Combination : Entity
#             | Combination Entity

# Alt         : Combination
#             | Alt OR Combination

# Bind        : NON_TERMINAL RULE Alt


@dataclass
class Terminal:
    value: str


@dataclass
class NonTerminal:
    value: str


@dataclass
class Null:
    pass


@dataclass
class Combination:
    values: List[Union[Terminal, NonTerminal, Null]]


@dataclass
class Alt:
    values: List[Union[Combination, Terminal, NonTerminal, Null]]


@dataclass
class Bind:
    name: str
    expr: Union[Alt, Combination, Terminal, NonTerminal, Null]


@dataclass
class Grammar:
    terminals: Set[str]
    non_terminals: Set[str]
    start: str
    rules: List[Bind]


def extract_terminals(expr: Union[Alt, Combination, Terminal, NonTerminal, Null]) -> Set[str]:
    if isinstance(expr, Alt) or isinstance(expr, Combination):
        return reduce(
            lambda result, items: result.union(items),
            map(extract_terminals, expr.values)
        )

    if isinstance(expr, Terminal):
        return { expr.value }

    if isinstance(expr, NonTerminal) or isinstance(expr, Null):
        return set()

    raise ValueError("Invalid expression provided!")


def extract_non_terminals(expr: Union[Alt, Combination, Terminal, NonTerminal, Null]) -> Set[str]:
    if isinstance(expr, Alt) or isinstance(expr, Combination):
        return reduce(
            lambda result, items: result.union(items),
            map(extract_non_terminals, expr.values)
        )

    if isinstance(expr, NonTerminal):
        return { expr.value }

    if isinstance(expr, Terminal) or isinstance(expr, Null):
        return set()

    raise ValueError("Invalid expression provided!")



def construct_grammar(start : str, rules : List[Bind]) -> Grammar:
    terminals = reduce(
        lambda result, current: result.union(current),
        map(lambda bind: extract_terminals(bind.expr), rules)
    )

    non_terminals = reduce(
        lambda result, current: result.union(current),
        map(lambda bind: extract_non_terminals(bind.expr), rules)
    )

    return Grammar(terminals, non_terminals, start, rules)


def construct_alt(
    left: Union[Alt, Combination, Terminal, NonTerminal, Null],
    right: Union[Combination, Terminal, NonTerminal, Null]
) -> Alt:
    if isinstance(left, Alt):
        return Alt(left.values + [ right ])

    return Alt([left, right])




def construct_combination(
    left: Union[Combination, Terminal, NonTerminal, Null],
    right: Union[Terminal, NonTerminal, Null],
) -> Combination:
    if isinstance(left, Combination):
        return Combination(left.values + [ right ])

    return Combination([left, right])



def p_grammar(p):
    "grammar : START Bindings"
    p[0] = construct_grammar(p[1], p[2])


def p_bindings(p):
    """
    Bindings : Bind
             | Bindings Bind
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_bind(p):
    "Bind : NON_TERMINAL RULE Alt SEPARATOR"
    p[0] = Bind(p[1], p[3])


def p_alt(p):
    """
    Alt : Alt OR Combination
        | Combination
    """
    if len(p) == 4:
        p[0] = construct_alt(p[1], p[3])
    else:
        p[0] = p[1]


def p_combination(p):
    """
    Combination : Entity
                | Combination Entity
    """
    if len(p) == 3:
        p[0] = construct_combination(p[1], p[2])
    else:
        p[0] = p[1]


def p_entity_terminal(p):
    "Entity : TERMINAL"
    p[0] = Terminal(p[1])


def p_entity_non_terminal(p):
    "Entity : NON_TERMINAL"
    p[0] = NonTerminal(p[1])


def p_entity_null(p):
    "Entity : NULL"
    p[0] = Null()


def p_error(p):
    if p is None:
        print("Unexpected end of input")
    else:
        token = f"{p.type}({p.value}) at {p.lineno}:{p.lexpos}"
        print(f"Syntax error: Unexpected {token}")
    exit()



parser = yacc.yacc()


def main():
    if len(sys.argv) > 1:
        filepath: str = sys.argv[1]
        with open(filepath, "r", encoding="utf-8") as code, open(
            filepath + ".out", "w", encoding="utf-8"
        ) as result:
            print(parser.parse("".join(code.readlines())), file=result)
    else:
        while True:
            print(parser.parse(input()))


if __name__ == "__main__":
    main()
