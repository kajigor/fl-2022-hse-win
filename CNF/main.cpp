#include "cnf.hpp"

int main() {
    cnf_grammar::Grammar grammar;
    std::string input = "another.txt.out"; // file with lexer grammar
    freopen("another_cnf.txt", "w", stdout);
    //std::cin >> input;
    std::ifstream is(input);
    is >> grammar;
    grammar.convert_to_CNF();
    grammar.print();
}
