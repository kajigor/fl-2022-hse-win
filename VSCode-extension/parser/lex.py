import ply.lex as lex
import sys

tokens = [
    'CHAR_SEQ_BEGIN',
    'BLANK_CHAR',
    'CHARACTER',
    'CLOSE',
    'STATE',
    'STATE_SEQ_BEGIN',
    'LINE_COMMENT',
    'BLOCK_COMMENT',
    'START',
    'CONTROL_COMMAND',
    'FUNCTION_SEQ_BEGIN',
    'FUNCTION_BEGIN',
    'FUNCTION_END',
    'FUNCTION_ARROW'
]

terminals = set()
nonTerminals = set()

ignoreComments = True


def t_LINE_COMMENT(t):
    r'//[^\n]*'
    global ignoreComments
    if ignoreComments:
        return
    # return t


def t_BLOCK_COMMENT(t):
    r'/\*(.|\n)*\*/'
    global ignoreComments
    t.lexer.lineno += t.value.count('\n')
    if ignoreComments:
        return
    # return t


def t_CONTROL_COMMAND(t):
    r'(left|right|stay)'
    return t


def t_FUNCTION_SEQ_BEGIN(t):
    r'Function{'
    return t


def t_FUNCTION_BEGIN(t):
    r'\('
    return t


def t_FUNCTION_END(t):
    r'\)'
    return t


def t_FUNCTION_ARROW(t):
    r'->'
    return t


def t_CHAR_SEQ_BEGIN(t):
    r'(Alphabet{|ExtraAlphabet{)'
    return t


def t_START(t):
    r'Start{'
    return t


def t_STATE_SEQ_BEGIN(t):
    r'(States{|Fail{|Success{)'
    return t


def t_BLANK_CHAR(t):
    r'Blank{'
    return t


def t_CHARACTER(t):
    r'[a-z][a-zA-Z0-9]*'
    return t


def t_STATE(t):
    r'[A-Z][a-zA-Z0-9]*'
    return t


t_ignore = ' \t'


def t_CLOSE(t):
    r'}'
    return t


def t_newline(t):
    r'\n'
    t.lexer.lineno += 1


def t_error(t):
    print('1 ' + str(t.lexer.lexpos) + ' 1' + '"Illegal character: ' + t.value[0] +'"')
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    # return t
    # exit(0)


lexer = lex.lex()


def main():
    # filename = sys.argv[1]
    # output = open(filename + '.out', 'w+')
    # data = open(filename).read()
    # data = s
    # lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
        # output.write(str(tok))
        # output.write('\n')


if __name__ == "__main__":
    main()
