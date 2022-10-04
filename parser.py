from ast import parse
from statistics import variance
import sys
from tkinter import Variable
import ply.yacc as yacc

from dataclasses import dataclass
from typing import List, Set, Union
from functools import reduce
from lexer import tokens


# Single      : EMPTY
#             | NON_TERMINAL
#             | TERMINAL
#
# Multiple    : Single
#             | Multiple Single
#
# Description : Multiple
#             | Description SEPARATOR Multiple
#
# Rule        : NON_TERMINAL ARROW Description END
#
# Ruleset     : Rule
#             | Ruleset Rule
#
# Start       : START 
#
# Root        : Start Ruleset

# Data classes
@dataclass
class Empty:
    pass

@dataclass
class NonTerminal:
    value: str

@dataclass
class Terminal:
    value: str

@dataclass
class Single:
    object: Union[Empty, NonTerminal, Terminal]

    def to_string(self) -> str:
        if (isinstance(self.object, Empty)):
            return "'ε'"
        return "'" + self.object.value + "'"


@dataclass
class Multiple:
    values: List[Single]

    def append(self, value: Single):
        self.values.append(value)
    
    def to_string(self) -> str:
        result: str = ""
        index = 0
        for single in self.values:
            result += single.to_string()
            index += 1
            if (index != len(self.values)):
                result += ", "
        return result

@dataclass
class Description:
    values: List[Multiple]

    def append(self, value: Multiple):
        self.values.append(value)
    
    def to_string(self) -> str:
        result: str = ""
        index = 0
        for multiple in self.values:
            result += "[" + multiple.to_string() + "]"
            index += 1
            if (index != len(self.values)):
                result += " | "
        return result

@dataclass 
class Rule:
    variable: NonTerminal
    desc: Description

    def to_string(self) -> str:
        return "'" + self.variable.value + "'" + " -> " + self.desc.to_string()

@dataclass
class Ruleset:
    rules: List[Rule]

    def append(self, rule: Rule):
        self.rules.append(rule)
    
        
    def to_string(self) -> str:
        result: str = ""
        for rule in self.rules:
            result += rule.to_string() + '\n'
        return result


@dataclass
class Start:
    variable: NonTerminal

    def to_string(self) -> str:
        return "'" + self.variable.value + "'"


@dataclass
class Root:
    start: Start
    ruleset: Ruleset

@dataclass
class Grammar:
    ast: Root
    terminals: Set[str]
    non_terminals: Set[str]

    def to_string(self) -> str:
        return f"""
-- Grammar --
Terminals: {sorted(self.terminals)}
Non-terminals: {sorted(self.non_terminals)}
Start: {self.ast.start.to_string()}
Rules:
{self.ast.ruleset.to_string()}
        """

# Parsing
def p_error(p):
    if p is None:
        print("Parser: Unexpected end of input")
    else:
        token = f"{p.type}({p.value}) at {p.lineno}:{p.lexpos}"
        print(f"Parser: Syntax error: Unexpected {token}", p)
    exit()


def p_root(p):
    """
        Root : Start Ruleset
    """
    print(f"p_root(): create Root({p[1]}, {p[2]})")
    p[0] = Root(p[1], p[2])


def p_start(p):
    """
        Start : START
    """
    print(f"p_start(): create Start({p[1]})")
    p[0] = Start(NonTerminal(p[1]))


def p_ruleset(p):
    """
        Ruleset : Rule
                | Ruleset Rule
    """
    if (len(p) == 2):
        print(f"p_ruleset(): {p[1]}")
        p[0] = Ruleset([p[1]])
    else:
        print(f"p_ruleset(): {p[1]}, {p[2]}")
        p[1].append(p[2])
        p[0] = p[1]

def p_rule(p):
    """
        Rule : NON_TERMINAL ARROW Description END
    """
    print(f"p_rule(): {p[1]}, {p[2]}, {p[3]}, {p[4]}")
    p[0] = Rule(NonTerminal(p[1]), p[3])

def p_description(p):
    """
        Description : Multiple
                    | Description SEPARATOR Multiple
    """
    if (len(p) == 2):
        print(f"p_description(): {p[1]}")
        p[0] = Description([p[1]])
    else:
        print(f"p_description(): {p[1]}, {p[2]}, {p[3]}")
        p[1].append(p[3])
        p[0] = p[1]

def p_multiple(p):
    """
        Multiple : Single
                 | Multiple Single
    """
    if (len(p) == 2):
        print(f"p_multiple(): {p[1]}")
        p[0] = Multiple([p[1]])
    else:
        print(f"p_multiple(): {p[1]}, {p[2]}")
        p[1].append(p[2])
        p[0] = p[1]

def p_single_empty(p):
    """
        Single : EMPTY
    """
    p[0] = Single(Empty())

def p_single_non_terminal(p):
    """
        Single : NON_TERMINAL
    """
    p[0] = Single(NonTerminal(p[1]))

def p_single_terminal(p):
    """
        Single : TERMINAL
    """
    p[0] = Single(Terminal(p[1]))

# Helper functions    
def get_terminals(ast: Root) -> Set[Terminal]:
    result: Set[Terminal] = set()

    for rule in ast.ruleset.rules:
        for multiple in rule.desc.values:
            for single in multiple.values:
                if (isinstance(single.object, Terminal)):
                    result.add(single.object.value)
    return result

def get_non_terminals(ast: Root) -> Set[NonTerminal]:
    result: Set[NonTerminal] = set()
    result.add(ast.start.variable.value)

    for rule in ast.ruleset.rules:
        result.add(rule.variable.value)

        for multiple in rule.desc.values:
            for single in multiple.values:
                if (isinstance(single.object, NonTerminal)):
                    result.add(single.object.value)
    return result

parser = yacc.yacc()

def main():
    if len(sys.argv) > 1:
        filepath: str = sys.argv[1]
        with open(filepath, "r", encoding="utf-8") as grammar_description, open(filepath + ".out", "w", encoding="utf-8") as output:
            ast: Root = parser.parse("".join(grammar_description.readlines()))
            grammar: Grammar = Grammar(ast, get_terminals(ast), get_non_terminals(ast))
            print(grammar.to_string(), file = output)
    else:
        while True:
            print(parser.parse(input("> ")))

if __name__ == "__main__":
    main()
