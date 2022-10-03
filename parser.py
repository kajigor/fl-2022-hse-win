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



Entity = Union[Terminal, NonTerminal, Null]



@dataclass
class Combination:
    values: List[Entity]

    def to_string(self, tabs='') -> str:
        result = "Combination(\n"

        for value in self.values:
            result += f"{tabs}\t{value},\n"

        result += f"{tabs})"
        return result



@dataclass
class Alt:
    values: List[Union[Combination, Entity]]

    def to_string(self, tabs='') -> str:
        result = "Alt(\n"
        inner_tabs = tabs + "\t"

        for value in self.values:
            if isinstance(value, Combination):
                result += f"{tabs}\t{value.to_string(inner_tabs)},\n"
            else:
                result += f"{tabs}\t{value},\n"

        result += f"{tabs})"

        return result


@dataclass
class Bind:
    name: str
    expr: Union[Alt, Combination, Entity]

    def to_string(self, additional_tabs='') -> str:
        tabs = "\t" + additional_tabs

        result = f"{additional_tabs}Bind " + "{\n"
        result += f"\tname: '{self.name}',\n"

        if isinstance(self.expr, Alt) or isinstance(self.expr, Combination):
            result += f"\texpr: {self.expr.to_string(tabs)}\n"
        else:
            result += f"\texpr: {self.expr}\n"

        result += f"{additional_tabs}" + "}"

        return result


@dataclass
class Grammar:
    terminals: Set[str]
    non_terminals: Set[str]
    start: str
    rules: List[Bind]

    def to_string(self) -> str:
        result = "-- Grammar -- \n\n"
        result += f"Terminals: {self.terminals}\n\n"
        result += f"Non-terminals: {self.non_terminals}\n\n"
        result += f"Start: '{self.start}'\n\n"

        result += "Rules: {\n"

        for rule in self.rules:
            result += rule.to_string('\t') + "\n"

        result += "}\n"

        return result



def extract_terminals(expr: Union[Alt, Combination, Entity]) -> Set[str]:
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


def extract_non_terminals(expr: Union[Alt, Combination, Entity]) -> Set[str]:
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



def is_correct_combination_values(value, start) -> bool:
    return isinstance(value, NonTerminal) and value != start



def is_correct_chomsky_value(start: str, expr:Union[Combination, Alt, Entity]) -> bool:
    if isinstance(expr, Entity):
        return not isinstance(expr, NonTerminal) # Null or Terminal -> true


    if isinstance(expr, Combination):
        return len(expr.values) == 2 \
               and is_correct_combination_values(expr.values[0], start) \
               and is_correct_combination_values(expr.values[1], start)

    if isinstance(expr, Alt):
        return all(map(lambda value: is_correct_chomsky_value(start, value), expr.values))



def is_null(expr : Union[Combination, Alt, Entity]) -> bool:
    if isinstance(expr, Entity):
        return isinstance(expr, Null)

    if isinstance(expr, Combination):
        return all(map(is_null, expr.values))

    if isinstance(expr, Alt):
        return any(map(is_null, expr.values))



def is_chomsky_normal_form(grammar : Grammar) -> bool:
    if any(map(lambda rule: rule.name != grammar.start and is_null(rule.expr), grammar.rules)):
        return False

    return all(map(lambda rule : is_correct_chomsky_value(grammar.start, rule.expr), grammar.rules))



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
    left: Union[Alt, Combination, Entity],
    right: Union[Combination, Entity]
) -> Alt:
    if isinstance(left, Alt):
        return Alt(left.values + [ right ])

    return Alt([left, right])




def construct_combination(
    left: Union[Combination, Entity],
    right: Entity,
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
        print(f"Syntax error: Unexpected {token}", p)
    exit()



parser = yacc.yacc()


def main():
    if len(sys.argv) > 1:
        filepath: str = sys.argv[1]
        with open(filepath, "r", encoding="utf-8") as code, open(
            filepath + ".out", "w", encoding="utf-8"
        ) as result:
            grammar=parser.parse("".join(code.readlines()))
            output = f"{grammar.to_string()}\nChomsky normal form: {is_chomsky_normal_form(grammar)}\n"

            print(output, file=result)
    else:
        while True:
            print(parser.parse(input()))


if __name__ == "__main__":
    main()
