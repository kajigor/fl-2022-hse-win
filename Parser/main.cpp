#include <iostream>
#include <string>
#include "parser.h"

using namespace std;

bool valid(string &path) {

    return !path.empty() && path != " ";
}

int main() {
    while (true) {
        string path;
        cin >> path;
        if (valid(path)) {
            parser::code program(path);
        } else {
            throw std::invalid_argument("Warning: Incorrect path.");
        }
    }
    return 0;
}
