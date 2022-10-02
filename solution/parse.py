import ply.yacc as yacc

precedence = (
  ('left', 'PLUS', 'MINUS'),
  ('left', 'MULT', 'DIV'),
  ('right', 'POW')
)

# Dangling-else problem
# if 0 then (if 1 then 777) else 9
# if : IF expr THEN if ELSE if
#    | IF expr THEN if
#    | expr
# expr : expr + expr
#      | expr - expr
#      | expr * expr
#      | expr / expr
#      | NUM
#      | LBR expr RBR

def p_if(p):
  '''if : IF expr THEN LBR if RBR ELSE LBR if RBR
        | IF expr THEN LBR if RBR
        | expr
  '''
  if len(p) == 11:
    p[0] = p[5] if p[2] == 0 else p[9]
  else:
    if len(p) == 7:
      p[0] = p[5] if p[2] == 0 else 9999999999999
    else:
      p[0] = p[1]

def p_expr_plus(p):
  'expr : expr PLUS expr'
  p[0] = p[1] + p[3]

def p_expr_minus(p):
  'expr : expr MINUS expr'
  p[0] = p[1] - p[3]

def p_expr_mult(p):
  'expr : expr MULT expr'
  p[0] = p[1] * p[3]

def p_expr_div(p):
  'expr : expr DIV expr'
  p[0] = p[1] / p[3]

def p_expr_pow(p):
  'expr : expr POW expr'
  p[0] = p[1] ** p[3]

def p_expr_num(p):
  'expr : NUM'
  p[0] = p[1]

def p_expr_br(p):
  'expr : LBR expr RBR'
  p[0] = p[2]

def p_error(p):
  if p == None:
    token = "end of file"
    parser.errok()
  else:
    token = f"{p.type}({p.value}) on line {p.lineno}"

  print(f"Syntax error: Unexpected {token}")

def main():
  parser = yacc.yacc()

  while True:
    try:
      s = input("calc> ")
    except EOFError:
      break
    if not s:
      continue
    result=parser.parse(s)
    print(result)

if __name__ == "__main__":
    main()





# def p_expr_plus(p):
#   'expr : expr PLUS term'
#   p[0] = p[1] + p[3]

# def p_expr_minus(p):
#   'expr : expr MINUS term'
#   p[0] = p[1] - p[3]

# def p_expr_term(p):
#   'expr : term'
#   p[0] = p[1]

# def p_term_mult(p):
#   'term : term MULT factor'
#   p[0] = p[1] * p[3]

# def p_term_div(p):
#   'term : term DIV factor'
#   p[0] = p[1] / p[3]

# def p_term_factor(p):
#   'term : factor'
#   p[0] = p[1]

# def p_factor_num(p):
#   'factor : NUM'
#   p[0] = p[1]

# def p_factor_br(p):
#   'factor : LBR expr RBR'
#   p[0] = p[2]


