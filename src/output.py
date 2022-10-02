def print_result(result, filename):
    with open(filename, "w") as fo:
        fo.write(result.pretty_print())
        if result.check_chomsky_form():
            fo.write(f"contextually free grammar in Chomsky's normal form ")
        else:
            fo.write("contextually free grammar not in Chomsky normal form")

def print_error(error_value, filename):
    with open(filename, "w") as fo:
        fo.write(f"Syntax error: {error_value}")
        