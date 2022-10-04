import ply.lex as lex
import sys

def replace_escape_symbols(a : str) -> str:
  a = a.replace("\$", "$")
  a = a.replace("\<", "<")
  a = a.replace("\>", ">")
  a = a.replace("\@", "@")
  a = a.replace("\_", "_")
  a = a.replace("\|", "|")
  a = a.replace("\;", ";")
  a = a.replace("\\\\", "\\")
  return a


reserved = {
  ';': 'SEP',
  '@': 'START',
  '_': 'EPS',
  '|' : 'OR'
}

tokens = [
  'TERM',
  'NONTERM',
  'BEGIN',
  'TO'
] + list(reserved.values())


def t_TERM(t):
  r'\$.+?\$'
  t.value = replace_escape_symbols(str(t.value[1:-1]))
  return t

def t_NONTERM(t):
  r'<.+?>'
  t.value = replace_escape_symbols(str(t.value[1:-1]))
  return t

def t_BEGIN(t):
  r'@<.+>;'
  t.value = replace_escape_symbols(str(t.value[2:-2]))
  return t

t_TO = r'->' 
t_SEP = r';'  
t_EPS = r'_'
t_OR = r'\|'
t_ignore = ' \t'

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

lexer = lex.lex()

def main():
	lexer = lex.lex()
	filename = sys.argv[1]
	with open(filename, 'r') as FIN:
		with open(filename + ".out", 'w') as FOUT:
			lexer.input("".join(FIN.readlines()))
			while True:
				tok = lexer.token()
				if not tok:
					break
				FOUT.write(str(tok) + '\n')

if __name__ == "__main__":
    main()