#include "cnf.hpp"

int main(int argc, char *argv[]) {
    if(argc != 3) {
        std::cout << "Two files should be provided\n" ;
        return 0;
    }
    std::string input = argv[1];// file with lexer grammar
    std::string output = argv[2];
    std::ifstream is(input);
    std::ofstream out(output);

    cnf_grammar::Grammar grammar;
    is >> grammar;

    grammar.convert_to_CNF();

    out << grammar;

}
