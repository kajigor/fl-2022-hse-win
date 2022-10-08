import sys
from typing import List

import ply.yacc as yacc
from output import print_result, print_error
 
 # Get the token map from the lexer.  This is required.
from lex import tokens

class Sequence:
    pass

class Block:
    pass

class OutputRule:
    def __init__(self, start_nonterm: str, sequence: Sequence):
        self.start_nonterm = start_nonterm
        self.sequence = sequence
    
    def pretty_print(self):
        result = f"({self.start_nonterm}) -> "
        result += self.sequence.pretty_print()
        return result
    
    def check_epsilon(self, start) -> bool:
        for block in self.sequence.lst:
            if (self.start_nonterm != start and len(block.lst) == 1 and block.lst[0].type == "EPS"):
                return False
        return True 
    
    def check_term_nterm(self):
        for block in self.sequence.lst:
            if ((len(block.lst) == 1 and block.lst[0].type != "TERM" and block.lst[0].type != "EPS")) or \
                     (len(block.lst) == 2 and (block.lst[0].type != "NONTERM" or block.lst[1].type != "NONTERM")) or \
                     (len(block.lst) > 2):
                return False
        return True 
    

class CFG:
    def __init__(self, start: str, description: List[OutputRule]):
        self.start = start
        self.description = description
    
    def pretty_print(self):
        result = f"Start nonterminal: {self.start}\n"
        for output_rule in self.description:
            res = output_rule.pretty_print()
            result += res + "\n"
        return result
    
    def check_chomsky_form(self) -> bool:
        for output_rule in self.description:
            if not all([output_rule.check_epsilon(self.start), output_rule.check_term_nterm()]):
                return False
        return True


class NonTerminal:
    def __init__(self, id: str):
        self.id = id
        self.type = "NONTERM"

class Terminal:
    def __init__(self, id: str):
        self.id = id
        self.type = "TERM"

class Epsilon:
    def __init__(self, id: str):
        self.id = id
        self.type = "EPS"

class Sequence:
    def __init__(self, element: Block):
        self.lst = [element]
    
    def merge(self, other: Sequence):
        self.lst += other.lst
    
    def pretty_print(self):
        result = ""
        if (len(self.lst) > 0):
            for i in range(0, len(self.lst) - 1):
                result += self.lst[i].pretty_print() + " | "
            result += self.lst[-1].pretty_print()
        return result

class Block:
    def __init__(self, value):
        self.lst = [value]

    def merge(self, other: Block):
        self.lst += other.lst
    
    def pretty_print(self):
        result = ""
        for element in self.lst:
            if element.type == "TERM":
                result += f"[{element.id}]"
            elif element.type == "NONTERM":
                result += f"({(element.id)})"
            else:
                result += f"{element.id}"
        return result

 
def p_expression(p):
    '''expression : start description'''
    p[0] = CFG(p[1], p[2])
    
def p_start(p):
    'start : START NONTERM LINEBREAK'
    p[0] = p[2]

def p_description(p):
    '''description : rule description
                   | empty '''
    if (p[1] is None):
        p[0] = []
    else:
        p[0] = [p[1]]
        if (p[2] is not None):
            p[0] += p[2]

def p_rule(p):
    '''rule : NONTERM ARROW sequence LINEBREAK'''
    p[0] = OutputRule(p[1], p[3])

def p_sequence(p):
    '''sequence : block 
                | block OR sequence
                '''
    p[0] = Sequence(p[1])
    if (len(p) > 2):
        p[0].merge(p[3])

def p_nonterm_block(p):
    '''block : NONTERM block
             | NONTERM
    '''
    p[0] = Block(NonTerminal(p[1]))
    if (len(p) > 2):
        p[0].merge(p[2])

def p_term_block(p):
    '''block : TERM block
             | TERM
    '''
    p[0] = Block(Terminal(p[1]))
    if (len(p) > 2):
        p[0].merge(p[2])

def p_eps_block(p):
    '''block : EPS block
             | EPS
    '''
    p[0] = Block(Epsilon(p[1]))
    if (len(p) > 2):
        p[0].merge(p[2])

def p_empty(p):
     'empty :'
     pass

 # Error rule for syntax errors
def p_error(p):
    print_error(p, filename + ".out")

 
 # Build the parser
parser = yacc.yacc()
 
filename = sys.argv[1]
try:
    file = open(filename)
except:
    pass

text = file.read()
result = parser.parse(text)
print_result(result, filename + ".out")
