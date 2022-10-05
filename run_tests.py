import sys

from lex import lex_from_file
from parse import parse_from_file
import os

for test in os.listdir('./tests'):

    if test.endswith('.txt'):
        file = './tests/' + test
        lex_from_file(file)
        print()
        sys.stdout.close()
        open(file + ".out", mode='a').write(parse_from_file(file))
