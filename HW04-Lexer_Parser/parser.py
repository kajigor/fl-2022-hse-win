import os
import sys
import ply.yacc

from lex import tokens
from lex import TokenError


class ParserError(Exception):
    pass


class Grammar:
    def __init__(self):
        self.__start = ""
        self.non_terminals = set()
        self.terminals = set()
        self.rules = []

    def add_term(self, elem: str):
        self.terminals.add(elem)

    def add_non_term(self, elem: str):
        self.non_terminals.add(elem)

    def add_rule(self, elem: str):
        self.rules.append(elem)

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, elem: str):
        if self.__start:
            raise ParserError("Invalid code: Several starts ...")
        self.__start = elem

    def __get_start(self) -> str:
        return f"Start: {self.__start}"

    def __get_terminals(self) -> str:
        return f"Terminals: {sorted(self.terminals)}"

    def __get_non_terminals(self) -> str:
        return f"Non terminals: {', '.join(sorted(self.non_terminals))}"

    def __get_rules(self) -> str:
        return "\n".join(
            [
                f"{vertex} -> {' | '.join([''.join(rule) for rule in rules])}"
                for vertex, rules in self.rules
            ]
        )

    def __str__(self):
        return (
            f"GRAMMAR\n\n"
            f"{self.__get_non_terminals()}\n"
            f"{self.__get_terminals()}\n"
            f"{self.__get_start()}\n\n"
            f"{self.__get_rules()}"
        )


GRAMMAR = Grammar()


def p_start(p):
    """expr : START"""
    p[0] = p[1]
    GRAMMAR.start = p[0]


def p_rule(p):
    """expr : NON_TERMINAL RULE desc END_OF_LINE"""
    p[0] = (p[1], p[3])
    GRAMMAR.add_rule(p[0])


def p_rule_description(p):
    """desc : concat"""
    p[0] = [p[1]]


def p_part_rule_description(p):
    """desc : desc SEPARATOR concat"""
    p[0] = p[1] + [p[3]]


def p_concat_elem(p):
    """concat : elem"""
    p[0] = [p[1]]


def p_concat_elems(p):
    """concat : concat elem"""
    p[0] = p[1] + [p[2]]


def p_token_term(p):
    """elem : TERMINAL"""
    p[0] = p[1]
    GRAMMAR.add_term(p[0])


def p_elem_non_terminal(p):
    """elem : NON_TERMINAL"""
    p[0] = p[1]
    GRAMMAR.add_non_term(p[0])


def p_elem_empty(p):
    """elem : EMPTY"""
    p[0] = p[1]


def p_error(p):
    if p is None:
        raise ParserError("Syntax error: Unexpected end of file ...")

    token = f"{p.type}({p.value}) on line {p.lineno}"
    raise ParserError(f"Syntax error: Unexpected {token}")


PARSER = ply.yacc.yacc()


def main():
    if len(sys.argv) == 1:
        exit("Args error: Waiting your file ...")

    if not os.path.exists(sys.argv[1]):
        exit("Args error: File not found ...")

    file_path = os.path.abspath(sys.argv[1])

    with open(file_path, "r", encoding="utf-8") as code_in, open(
        f"{file_path}.out", "w"
    ) as code_out:
        for line in code_in.readlines():
            try:
                PARSER.parse(line)
            except (ParserError, TokenError) as e:
                exit(*e.args)

        print(GRAMMAR, file=code_out)

    print("File is processed ...")


if __name__ == "__main__":
    main()
