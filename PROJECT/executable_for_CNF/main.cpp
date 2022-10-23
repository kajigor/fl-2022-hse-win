#include "cnf.hpp"

int main(int argc, char *argv[]) {
    if(argc != 4) {
        return 0;
    }

    std::string input = argv[1];// file with lexer grammar
    std::string output = argv[2];
    std::string outputLong = argv[3];
    std::ifstream is(input);
    std::ofstream out(output);
    std::ofstream outLong(outputLong);

    cnf_grammar::Grammar grammar;
    is >> grammar;

    grammar.convert_to_CNF(outLong);
    out << grammar;

}
