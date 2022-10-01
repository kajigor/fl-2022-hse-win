import ply.yacc as yacc
import sys

from dataclasses import dataclass
from typing import List, Set, Union
from grammarlex import tokens
from functools import reduce

# primitive : TERMINAL
#           | NON_TERMINAL
#           | EPS   
# cons : primitive
#      | cons primitive 
# alt : cons
#     | alt ALT cons
# bind : NON_TERMINAL BINDING alt

@dataclass
class Eps:
    pass

eps = Eps()  

@dataclass
class Terminal:
    value : str

@dataclass
class NonTerminal:
    value : str

@dataclass
class Cons:
    vals : List[Union[Terminal, NonTerminal, Eps]]

def make_cons(lhs : Union[Cons, Terminal, NonTerminal, Eps],
              rhs : Union[Terminal, NonTerminal, Eps]) -> Cons:
    if isinstance(lhs, Cons):
        return Cons(lhs.vals + [rhs])
    return Cons([lhs, rhs])

@dataclass
class Alt:
    vals : List[Union[Cons, Terminal, NonTerminal, Eps]]

def make_alt(lhs : Union[Alt, Cons, Terminal, NonTerminal, Eps],
             rhs : Union[Cons, Terminal, NonTerminal, Eps]) -> Alt:
    if isinstance(lhs, Alt):
        return Alt(lhs.vals + [rhs])
    return Alt([lhs, rhs])
    
@dataclass
class Binding:
    name : str
    expr : Union[Alt, Cons, Terminal, NonTerminal, Eps]
    

@dataclass
class CFG:
    terminals : Set[str]
    non_terminals : Set[str]
    start : str
    rules : List[Binding]


def collect_non_terminals(expr : Union[Eps, Terminal, NonTerminal, Cons, Alt]) -> Set[str]:
    if isinstance(expr, Eps) or isinstance(expr, Terminal):
        return set()
    elif isinstance(expr, NonTerminal):
        return {expr.value}
    elif isinstance(expr, Cons) or isinstance(expr, Alt):
        return reduce(lambda lhs, rhs: lhs | rhs, map(collect_non_terminals, expr.vals))
    else:
        raise ValueError("Expression is not valid")


def collect_terminals(expr : Union[Eps, Terminal, NonTerminal, Cons, Alt]) -> Set[str]:
    if isinstance(expr, Eps) or isinstance(expr, NonTerminal):
        return set()
    elif isinstance(expr, Terminal):
        return {expr.value}
    elif isinstance(expr, Cons) or isinstance(expr, Alt):
        return reduce(lambda lhs, rhs: lhs | rhs, map(collect_terminals, expr.vals))
    else:
        raise ValueError("Expression is not valid")

def make_grammar(start : str, rules : List[Binding]) -> CFG:
    terminals = reduce(lambda lhs, rhs: lhs | rhs,
                           map(lambda binding: collect_terminals(binding.expr),
                               rules))
    non_terminals = (reduce(lambda lhs, rhs: lhs | rhs,
                           map(lambda binding: collect_non_terminals(binding.expr),
                               rules))
                    | set(map(lambda binding: binding.name, rules)))
    return CFG(terminals, non_terminals, start, rules)


def is_nullable(expr : Union[Eps, Terminal, NonTerminal, Cons, Alt]) -> bool:
    if isinstance(expr, Eps):
        return True
    elif isinstance(expr, NonTerminal):
        return False
    elif isinstance(expr, Terminal):
        return False
    elif isinstance(expr, Cons):
        return all(map(is_nullable, expr.vals))
    elif isinstance(expr, Alt):
        return any(map(is_nullable, expr.vals))
    else:
        raise ValueError("Expression is not valid")

def is_chomsky_rvalue(start : str, expr : Union[Eps, Terminal, NonTerminal, Cons, Alt]) -> bool:
    if isinstance(expr, Eps):
        return True
    elif isinstance(expr, NonTerminal):
        return False
    elif isinstance(expr, Terminal):
        return True
    elif isinstance(expr, Cons):
        return (len(expr.vals) == 2
               and isinstance(expr.vals[0], NonTerminal)
               and isinstance(expr.vals[1], NonTerminal)
               and expr.vals[0].value != start
               and expr.vals[1].value != start)
    elif isinstance(expr, Alt):
        return all(map(lambda val: is_chomsky_rvalue(start, val), expr.vals))
    else:
        raise ValueError("Expression is not valid")
 
    

def is_chomsky_nf(grammar : CFG) -> bool:
    if any(map(lambda rule: rule.name != grammar.start and is_nullable(rule.expr), grammar.rules)):
        return False
    return all(map(lambda rule : is_chomsky_rvalue(grammar.start, rule.expr), grammar.rules))


def show_expr(expr : Union[Eps, Terminal, NonTerminal, Cons, Alt]) -> str:
    if isinstance(expr, Eps):
        return "EPS"
    elif isinstance(expr, NonTerminal):
        return f"<{expr.value}>"
    elif isinstance(expr, Terminal):
        return f"`{expr.value}`"
    elif isinstance(expr, Cons):
        return "".join(map(show_expr, expr.vals))
    elif isinstance(expr, Alt):
        return " | ".join(map(show_expr, expr.vals))
    else:
        raise ValueError("Expression is not valid")

def show(grammar : CFG) -> str:
    result = "Context Free Grammar:\n"
    result += f"Terminal characters are {grammar.terminals}\n"
    result += f"Non-terminal characters are {grammar.non_terminals}\n"
    result += f"Start non-terminal is <{grammar.start}>\n\n"
    result += "Rules:\n"
    result += "\n".join(map(lambda binding: binding.name + " := " + show_expr(binding.expr), grammar.rules)) + "\n"
    result += "\n\nraw:\n" + str(grammar) + "\n\n"
    if is_chomsky_nf(grammar):
        result += "This grammar is in chomsky normal form\n"
    else:
        result += "This grammar is not in chomsky normal form\n"
    return result

start = "grammar"

def p_grammar(p):
    'grammar : START bindings'
    p[0] = make_grammar(p[1], p[2])

def p_bindings(p):
    '''bindings : bind
                | bindings bind
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_binding(p):
    'bind : NON_TERMINAL BINDING alt SEP'
    p[0] = Binding(p[1], p[3])

def p_alt(p):
    '''alt : alt ALT cons
           | cons
    '''
    if len(p) == 4:
        p[0] = make_alt(p[1], p[3])
    else:
        p[0] = p[1]
 
def p_cons(p):
    '''cons : primitive
            | cons primitive
    '''
    if len(p) == 3:
        p[0] = make_cons(p[1], p[2])
    else:
        p[0] = p[1]

def p_primitive_terminal(p):
    'primitive : TERMINAL'
    p[0] = Terminal(p[1])

def p_primitive_non_terminal(p):
    'primitive : NON_TERMINAL'
    p[0] = NonTerminal(p[1])

def p_primitive_eps(p):
    'primitive : EPS'
    p[0] = eps

def p_error(p):
    if p == None:
        print("Unexpected end of input")
    else:
        token = f"{p.type}({p.value}) at {p.lineno}:{p.lexpos}"
        print(f"Syntax error: Unexpected {token}")
    exit()


parser = yacc.yacc()

def main():
    if(len(sys.argv) > 1):
        filename : str = sys.argv[1]
        with open(filename, 'r') as code, open(filename + ".out", "w") as result:
            print(show(parser.parse("".join(code.readlines()))), file = result)       
    else:
      while True:
          print(parser.parse(input()))

if __name__ == "__main__":
    main()



