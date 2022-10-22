//
// Created by Boris Mikhaylov on 2022-10-22.
//

#include <string>
#include <vector>

#ifndef TURINGPROJECT_PARSER_H
#define TURINGPROJECT_PARSER_H

using namespace std;

namespace parser {
    struct code {
        vector<string> lines;

        [[maybe_unused]] explicit code(string &input_file) {
            delete_comments_1(input_file);
            lines = split(input_file, '\n');
            delete_comments_2();
        }
        
    private:
        /*
         * splits input string into single lines divided by \n
         */
        static vector<string> split(const string &str, char separator) {
            vector<string> ans;
            size_t end = 0;
            while (int start = str.find_first_not_of(separator, end) != std::string::npos) {
                end = str.find(separator, start);
                ans.push_back(str.substr(start, end - start));
            }
            return ans;
        }

        /*
         * removes multiline comments
         * todo: make warning show line and symbol number at exception
         * iterator should be over the list of lines so we can check
         * position of issue. afterwards needed to swap filling lines
         * and removing of block comments.
         */
        static void delete_comments_1(string &str) {
            auto start = str.begin(), end = str.begin();
            bool opened = false;
            bool closed = false;
            while (end != str.end()) {
                if (end + 1 != str.end() && *end == '/' && *(end + 1) == '*') opened = true;
                if (end + 1 != str.end() && *end == '*' && *(end + 1) == '/') closed = true;
                if (closed && !opened) throw std::invalid_argument("Warning ");
                if (opened && closed) {
                    str.erase(start, end);
                    start = end;
                    opened = false;
                    closed = false;
                }
                if (opened < closed) throw std::invalid_argument("Warning");
            }
        }

        /*
         * removes remaining one-liner comments
         */
        void delete_comments_2() {
            for (auto &l: lines) {
                for (int i = 0; i < l.size() - 1; ++i) {
                    if (l[i] == '/' && l[i + 1] == '/') {
                        l = l.substr(0, i);
                        break;
                    }
                }
            }
        }
    };
}

#endif //TURINGPROJECT_PARSER_H
