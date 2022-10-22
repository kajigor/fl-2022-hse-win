from enum import Enum
import argparse
import sys

class TuringMachine:
    class Rules:
        def __init__(self, transitions):
            self.transitions = transitions

        def value(self, state, symbol):
            return self.transitions[state][symbol]

    class Movement(Enum):
        N = 1
        P = -1

    def __init__(self, states, in_alph, tp_alph, start, end, rules_fun):
        self.states = states
        self.in_alph = in_alph
        self.tp_alph = tp_alph
        self.start = start
        self.end = end
        self.rules_fun = self.Rules(rules_fun)

        self.check_valid()

    def check_valid(self):
        if not self.in_alph.issubset(self.tp_alph):
            print("Entry alphabet is not a subset of tape alphabet")
            sys.exit(0)
        elif self.start not in self.states:
            print("Start state is not in states set")
            sys.exit(0)
        elif not self.end.issubset(self.states):
            print("Start state is not in states set")
            sys.exit(0)

    def is_valid(self, string):
        for s in string:
            if s not in self.in_alph:
                print("Entry string is not a subset of alphabet")
                sys.exit(0)

    def rules(self, configuration):
        actual_state, string, position = configuration
        new_state, substitution, direction = self.rules_fun.value(actual_state, string[position])
        string[position] = substitution
        position += self.Movement[direction].value
        
        return (new_state, string, position)

    def print_step(self, configuration):
        state, string, position = configuration
        print("{:10s} {} {:3d}".format(state, "|".join(string), position))

    def accepts(self, string, verbose=False, steps=1000000):
        string = list("_" + string + "_")
        configuration = (self.start, string, 1)
        if verbose:
            print("_____________SOLUTION______________")
            print("{:10s} {} {:3s}".format("State", "Configuration", "Position"))
            self.print_step(configuration)
        while configuration[0] not in self.end and steps > 1:
            steps -= 1
            try:
                configuration = self.rules(configuration)
            except KeyError:
                return False
            if verbose:
                self.print_step(configuration)
        return True

    def n_language(self, n):
        if n <= 0:
            yield ""
        else:
            for s in self.in_alph:
                for w in self.n_language(n-1):
                    yield s + w 

    def language(self):
        n = 0
        while(True):
            for w in self.n_language(n):
                yield w
            n += 1

    def accepted_language(self):
        language = self.language()
        for w in language:
            if self.accepts(w):
                yield w

def parse(f):
    #a simple parser and simple syntax, as long as Denis does the right one
    f = open(f)
    states = set()
    in_alph = set()
    tp_alph = set()
    end = set()
    rules = {}
    for _ in range(int(f.readline())):
        states.add(f.readline().rstrip("\n"))
    for _ in range(int(f.readline())):
        in_alph.add(f.readline().rstrip("\n"))
    for _ in range(int(f.readline())):
        tp_alph.add(f.readline().rstrip("\n"))
    start = f.readline().rstrip("\n")
    for _ in range(int(f.readline())):
        end.add(f.readline().rstrip("\n"))
    for q in states:
        rules[q] = {}
    for _ in range(int(f.readline())):
        st_sym, triplet = f.readline().split(":")
        state, symbol = st_sym.strip().split(" ")
        result = tuple(triplet.strip().split(" "))
        rules[state][symbol] = result
    f.close()
    return TuringMachine(states, in_alph, tp_alph, start, end, rules)
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="Rules file", required=True)
    parser.add_argument("-i", help="String to be run with the Turing machine")
    parser.add_argument("-v", help="Prints step-by-step", action="store_true")
    parser.add_argument("-k", help="Prints only k steps")
    args = parser.parse_args()

    tm = parse(args.f)

    if args.i:
        tm.is_valid(args.i)
        if args.k:
            result = "" if tm.accepts(args.i, args.v, int(args.k)) else "NOT "
        else:
            result = "" if tm.accepts(args.i, args.v) else "NOT "
            print("The string '{}' is {}accepted by the Turing machine".format(args.i, result))
