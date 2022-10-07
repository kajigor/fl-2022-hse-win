from audioop import mul
from dataclasses import dataclass
from sys import argv
from typing import List, Set, Union
import ply.yacc as yacc
from lex import tokens

"""
rules    : rule
         | rules rule

rule     : NTERM BIND one_more END_OF_RULE

one_more : multiple
         | multiple OR one_more

multiple : single
         | multiple SEP single

single   : TERM
         | NTERM
         | EPSILON
"""

isStart = False
Start: Union[str, None] = None


@dataclass
class Terminal:
    name: str

    def __init__(self, name: str):
        self.name = name.strip("#")


@dataclass
class NonTerminal:
    name: str

    def __init__(self, name: str):
        self.name = name.strip("$")


@dataclass
class Start:
    name: str


@dataclass
class Empty:
    name = ""


@dataclass
class Single:
    value:  Union[Empty, NonTerminal, Terminal]


@dataclass
class Multiple:
    values: List[Single]

    def append(self, other):
        self.values.append(other)

    def to_string(self):
        res = ""

        for single in self.values:
            res += single.value.name + " "

        res = res.strip()
        return res


@dataclass
class OneMore:
    values: List[Multiple]

    def append(self, other):
        self.values.append(other)

    def to_string(self):
        res = ""

        for multiple in self.values:
            res += multiple.to_string() + " | "

        res = res.strip(" |")
        return res


@dataclass
class Rule:
    nt: NonTerminal
    mapsto: OneMore

    def to_string(self):
        res = f"\t {self.nt.name} --> [ {self.mapsto.to_string()} ]"

        return res


RULES: List[Rule] = []


def p_rules(p):
    """
    rules : rule
          | rules rule
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].append(p[2])
        p[0] = p[1]


def p_rule(p):
    "rule : NTERM BIND one_more END_OF_RULE"

    rule = Rule(NonTerminal(p[1]), p[3])
    RULES.append(rule)
    p[0] = rule


def p_one_more(p):
    """
    one_more : multiple
             | one_more OR multiple
    """
    if len(p) == 2:
        p[0] = OneMore([p[1]])
    else:
        p[1].append(p[3])
        p[0] = p[1]


def p_multiple(p):
    """
    multiple : single
             | multiple SEP single
    """
    if len(p) == 2:
        p[0] = Multiple([p[1]])
    else:
        p[1].append(p[3])
        p[0] = p[1]


def p_single_t(p):
    """
    single : TERM
    """
    p[0] = Single(Terminal(p[1]))


def p_single_nt(p):
    """
    single : NTERM
    """

    nt = NonTerminal(p[1])

    global Start, isStart
    if not isStart:
        Start = nt.name
        isStart = True

    p[0] = Single(nt)


def p_single_e(p):
    """
    single : EPSILON
    """
    p[0] = Single(Empty())


def extract_terminals() -> Set[str]:
    terminals = set()

    for rule in RULES:
        for values in rule.mapsto.values:
            for single in values.values:
                if isinstance(single.value, Terminal):
                    terminals.add(single.value.name)

    return terminals


def extract_non_terminals() -> Set[str]:
    nterminals = set()

    for rule in RULES:
        if (rule.nt.name != "start"):
            nterminals.add(rule.nt.name)

            for values in rule.mapsto.values:
                for single in values.values:
                    if isinstance(single.value, NonTerminal):
                        nterminals.add(single.value.name)

    return nterminals


def isNonTerminal(who):
    return isinstance(who, NonTerminal)


def isTerminal(who):
    return isinstance(who, Terminal)


def isEmpty(who):
    return isinstance(who, Empty)


def is_chomsky_form():
    for rule in RULES:
        if (rule.nt.name == "start"): continue
        for multiple in rule.mapsto.values:
            values = multiple.values
            length = len(values)
            if length > 2:
                return False
            if length == 2 and not (isNonTerminal(values[0].value) and isNonTerminal(values[0].value)):
                return False
            if length == 1 and not ((isTerminal(values[0].value)) or (isEmpty(values[0].value) and rule.nt.name == Start)):
                print(isEmpty(values[0].value), rule.nt.name)
                return False
    return True


global parser


def p_error(p):
    if p == None:
        token = "end of file"
        parser.errok()
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")


parser = yacc.yacc()


def main():
    with open(argv[1], "r") as grammar, open(argv[1] + ".out", "w") as result:
        file = grammar.readlines()
        for line in file:
            parser.parse(line)
        print(f"Start non-terminal: {Start}", file=result)
        print(f"Non-terminals: {sorted(extract_non_terminals())}", file=result)
        print(f"Terminals: {sorted(extract_terminals())}", file=result)
        print("Rules: {\n", file=result)
        for rule in RULES:
            print(rule.to_string() + "\n", file=result)
        print("}", file=result)
        print('The grammar is in Chomsky Normal Form:', is_chomsky_form(), file=result)


if __name__ == "__main__":
    main()
