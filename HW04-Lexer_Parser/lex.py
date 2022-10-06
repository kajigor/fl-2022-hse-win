import sys
import os
import ply
import ply.lex


class TokenError(Exception):
    pass


tokens = [
    "START",
    "TERMINAL",
    "NON_TERMINAL",
    "SEPARATOR",
    "EMPTY",
    "RULE",
    "END_OF_LINE",
]

t_SEPARATOR = r"\~"
t_RULE = r"\<\<\>\<\>\>"
t_EMPTY = r"\%\%\%\%\%"
t_END_OF_LINE = r"\|\|\|\|\|"

t_ignore = " \t"


def __include_symbols(value: str) -> str:
    return (
        value.replace("\\&", "&")
        .replace("\\@", "@")
        .replace("\\~", "~")
        .replace("\\\\", "\\")
    )


def t_newline(t: ply.lex.LexToken):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_START(t: ply.lex.LexToken):
    r"""\-\-\>@.+?(?<!(?<!\\)\\)@"""
    t.value = t.value[4:-1]
    return t


def t_error(t: ply.lex.LexToken):
    raise TokenError(f"Syntax error: Illegal character '{t.value[0]}'.")


def t_TERMINAL(t: ply.lex.LexToken):
    r"""&.+?(?<!\\)&"""
    t.value = __include_symbols(t.value[1:-1])
    return t


def t_NON_TERMINAL(t: ply.lex.LexToken):
    r"""@.+?(?<!(?<!\\)\\)@"""
    t.value = __include_symbols(t.value[1:-1])
    return t


lexer = ply.lex.lex()


def main():
    if len(sys.argv) == 1:
        exit("Waiting your file ...")

    if not os.path.exists(sys.argv[1]):
        exit("File not found ...")

    file_path = os.path.abspath(sys.argv[1])

    with open(file_path, "r", encoding="utf-8") as read_lang, open(
        file_path + ".out", "w"
    ) as write_lang:
        for line in read_lang.readlines():
            lexer.input(line.rstrip())

            while True:

                try:
                    token = lexer.token()
                except TokenError as e:
                    exit(*e.args)

                if not token:
                    break

                print(token, file=write_lang)

    print("File is processed ...")


if __name__ == "__main__":
    main()
