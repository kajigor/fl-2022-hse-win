import ply.lex as lex
import sys

tokens = [
    'LINE_COMMENT',
    'BLOCK_COMMENT',
    'ALPHABET',
    'EXTRA_ALPHABET',
    'STATES',
    'FUNCTION',
    'SUCCESS',
    'FAIL',
    'START',
    'BLANK',
    'LEFT',
    'RIGHT',
    'STAY',
    'STATE_NAME',
    'CHAR_NAME',
    'BEGIN_SEQ',
    'END_SEQ',
    'BEGIN_TRANS',
    'END_TRANS',
    'FUNCTION_ARROW'
]

ignoreComments = True


def t_LINE_COMMENT(t):
    r'//[^\n]*'
    global ignoreComments
    if ignoreComments:
        return
    return t


def t_BLOCK_COMMENT(t):
    r'/\*([^\*]|\*[^/])*\*/'
    global ignoreComments
    t.lexer.lineno += t.value.count('\n')
    if ignoreComments:
        return
    return t


def t_ALPHABET(t):
    r'Alphabet'
    return t


def t_EXTRA_ALPHABET(t):
    r'ExtraAlphabet'
    return t


def t_STATES(t):
    r'States'
    return t


def t_FUNCTION(t):
    r'Function'
    return t


def t_SUCCESS(t):
    r'Success'
    return t


def t_FAIL(t):
    r'Fail'
    return t


def t_START(t):
    r'Start'
    return t


def t_BLANK(t):
    r'Blank'
    return t


def t_LEFT(t):
    r'left'
    return t


def t_RIGHT(t):
    r'right'
    return t


def t_STAY(t):
    r'stay'
    return t


def t_BEGIN_SEQ(t):
    r'\{'
    return t


def t_END_SEQ(t):
    r'\}'
    return t


def t_BEGIN_TRANS(t):
    r"""\("""
    return t


def t_END_TRANS(t):
    r"""\)"""
    return t


def t_FUNCTION_ARROW(t):
    r'->'
    return t


def t_CHAR_NAME(t):
    r'[a-z][a-zA-Z0-9]*'
    return t


def t_STATE_NAME(t):
    r'[A-Z][a-zA-Z0-9]*'
    return t


t_ignore = ' \t'


def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.linepos = t.lexer.lexpos


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    # return t
    # exit(0)


def create_lexer():
    return lex.lex()


lexer = lex.lex()


def main():
      filename = 'input.txt'
      output = open(filename + '.out', 'w+')
      data = open(filename).read()
      #data = s
      lexer.input(data)

      while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
        # output.write(str(tok))
        # output.write('\n')


if __name__ == "__main__":
    main()
