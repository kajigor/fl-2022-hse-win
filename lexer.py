# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring, invalid-name, missing-module-docstring, consider-using-f-string
import sys
import ply.lex as lex

tokens = [
    "OR",
    "RULE",
    "NULL",
    "SEPARATOR",
    "TERMINAL",
    "NON_TERMINAL",
    "START",
]


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Unexpected character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)


# defining tokens
t_OR = r"\|"
t_RULE = r"->"
t_NULL = r"NULL"
t_SEPARATOR = r";"
t_ignore = " \t"


def t_TERMINAL(token):
    r"'.+?(?<!\\)'"
    token.value = remove_escape(token.value[1:-1])
    return token


def t_NON_TERMINAL(token):
    r"\$(\S+(?<!(?!<\\)\\|\$))"
    token.value = remove_escape(token.value[1:])
    return token


def t_START(token):
    r"start=\$(\S+(?<!(?!<\\)\\|\$))"
    token.value = remove_escape(token.value[7:])
    return token


# helpers
def remove_escape(string: str) -> str:
    return string.replace("\\$", "$").replace("\\\\", "\\")



lexer = lex.lex()


def main():
    if len(sys.argv) > 1:
        filename: str = sys.argv[1]

        with open(filename, "r", encoding="utf-8") as code, open(
            filename + ".out", "w", encoding="utf-8"
        ) as output:
            lexer.input("".join(code.readlines()))

            while token := lexer.token():
                print(token, file=output)
    else:
        while True:
            lexer.input(input("> "))

            while token := lexer.token():
                print(token)


if __name__ == "__main__":
    main()
