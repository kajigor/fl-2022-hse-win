import ply.yacc as yacc
import sys

from lex import tokens

# RULE : NOT_TERMINAL IMPLICATION ONE_MORE
#      | INIT_TOKEN IMPLICATION ONE_MORE
# INIT_TOKEN : INITIAL
# ONE_MORE : EPSILON ONE_MORE
# ONE_MORE : TERMINAL ONE_MORE
# ONE_MORE : NOT_TERMINAL ONE_MORE
# ONE_MORE : EPSILON
# ONE_MORE : TERMINAL
# ONE_MORE : NOT_TERMINAL

not_terminals = set()
terminals = set()
rules = []
initial = None
output_file = None
find_init = False


def p_RULE(p):
    '''RULE : NOT_TERMINAL IMPLICATION ONE_MORE
          | INIT_TOKEN IMPLICATION ONE_MORE '''
    p[0] = [p[1], p[3]]
    global find_init, initial
    if not find_init:
        initial = p[1]
        find_init = True
    rules.append([p[1], p[3]])
    not_terminals.add(p[1])

def p_init(p):
    'INIT_TOKEN : INITIAL'
    global initial
    initial = p[1]
    p[0] = p[1]



def p_ONE_MORE_EPSILON(p):
    'ONE_MORE : EPSILON ONE_MORE'
    p[0] = p[2]


def p_ONE_MORE_TERMINAL(p):
    'ONE_MORE : TERMINAL ONE_MORE'
    global terminals
    terminals.add(p[1])
    p[0] = p[1] + p[2]


def p_ONE_MORE_NOT_TERMINAL(p):
    'ONE_MORE : NOT_TERMINAL ONE_MORE'
    global not_terminals
    not_terminals.add(p[1])
    p[0] = p[1] + p[2]

def p_ONE_MORE_ONLY_EPSILON(p):
    'ONE_MORE : EPSILON'
    p[0] = p[1]


def p_ONE_MORE_ONLY_TERMINAL(p):
    'ONE_MORE : TERMINAL'
    global terminals
    terminals.add(p[1])
    p[0] = p[1]


def p_ONE_MORE_ONE_NOT_TERMINAL(p):
    'ONE_MORE : NOT_TERMINAL'
    global not_terminals
    not_terminals.add(p[1])
    p[0] = p[1]

def p_error(p):
    if not p is None:
        print(f"Lexical error in '%s' at line {p.lineno}" % p.value[0], file=output_file)


parser = yacc.yacc()


def main():
    file = open(sys.argv[1], 'r')
    global output_file
    output_file = open(sys.argv[1] + ".out", 'w')
    for line in file:
        parser.parse(line)
    print("Начальный нетерминал: " + initial, file=output_file)
    print("Терминалы:", file=output_file)
    for terminal in terminals:
        print('\t' +terminal, file=output_file)
    print("Нетерминалы:", file=output_file)
    for not_terminal in not_terminals:
        print('\t' + not_terminal, file=output_file)
    print("Правила КС грамматики:", file=output_file)
    for rule in rules:
        print('\t' + rule[0] + " --->  " + rule[1], file=output_file)
    output_file.close()



if __name__ == "__main__":
    main()
