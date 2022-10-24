#!/usr/bin/env python3
import sys

import ply.yacc as yacc

import lex
from lex import tokens
from turing import TuringMachine

start = 'turing_machine'


def p_char_sequence(p):
    """
    char_sequence : CHAR_NAME
                  | char_sequence CHAR_NAME
    """
    if len(p) == 2:
        p[0] = [p.slice[1]]
    else:
        p[1].append(p.slice[2])
        p[0] = p[1]


def p_state_sequence(p):
    """
    state_sequence : STATE_NAME
                   | state_sequence STATE_NAME
    """
    if len(p) == 2:
        p[0] = [p.slice[1]]
    else:
        p[1].append(p.slice[2])
        p[0] = p[1]


def p_alphabet(p):
    """alphabet : ALPHABET BEGIN_SEQ char_sequence END_SEQ"""
    p[0] = p[3]


def p_extra_alphabet(p):
    """extra_alphabet : EXTRA_ALPHABET BEGIN_SEQ char_sequence END_SEQ"""
    p[0] = p[3]


def p_states(p):
    """states : STATES BEGIN_SEQ state_sequence END_SEQ"""
    p[0] = p[3]


def p_blank(p):
    """blank : BLANK BEGIN_SEQ CHAR_NAME END_SEQ"""
    p[0] = p.slice[3]


def p_start(p):
    """start : START BEGIN_SEQ STATE_NAME END_SEQ"""
    p[0] = p.slice[3]


def p_fail(p):
    """fail : FAIL BEGIN_SEQ state_sequence END_SEQ"""
    p[0] = p[3]


def p_success(p):
    """success : SUCCESS BEGIN_SEQ state_sequence END_SEQ"""
    p[0] = p[3]


def p_direction(p):
    """direction : LEFT
                 | STAY
                 | RIGHT"""
    p[0] = p.slice[1]


def p_transfer(p):
    """transfer : BEGIN_TRANS STATE_NAME CHAR_NAME FUNCTION_ARROW STATE_NAME CHAR_NAME direction END_TRANS"""
    p[0] = [p.slice[2], p.slice[3], p.slice[5], p.slice[6], p[7]]


def p_transfer_sequence(p):
    """
    transfer_sequence : transfer
                      | transfer_sequence transfer
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]


def p_function(p):
    """function : FUNCTION BEGIN_SEQ transfer_sequence END_SEQ"""
    p[0] = p[3]


def p_turing_machine(p):
    """turing_machine : alphabet extra_alphabet states blank start fail success function"""
    p[0] = TuringMachine(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])


def p_error(p):
    if p is None:
        token = "end of file"
        parser.errok()
        return
    else:
        print('Unexpected token ' + p.value + ' at ' + str(p.lineno) + ':' + str(p.lexpos - p.lexer.linepos + 1))
        exit(0)


parser = yacc.yacc()


def parse_grammar(text):
    return parser.parse(text, lex.create_lexer())


def main():
    global NICE_DIAGNOSTICS, DISABLE_DIAGNOSTICS
    args = sys.argv
    out = parse_grammar(open(args[1], 'r').read())

    out.run(args[2:])


if __name__ == "__main__":
    main()
