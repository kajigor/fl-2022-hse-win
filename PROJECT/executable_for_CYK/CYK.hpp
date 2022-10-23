#ifndef CYK_HPP_
#define CYK_HPP_

#include <cassert>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>

namespace cyk_algorithm {

class Matrix {

private:
  std::vector<std::vector<std::vector<std::string>>> matrix;
  std::vector<int> columnsSize;
  int size;

public:
  Matrix(int n) : size(n) {
    matrix.assign(n, std::vector<std::vector<std::string>>(n));

    columnsSize.resize(n, 0);
  }

  [[nodiscard]] int get_size() const;
  void print_matrix(std::ofstream &fout);
  void insert_in_cell(int row, int column,
                      const std::vector<std::string> &new_cell);
  std::vector<std::string> get_cell(int row, int column);
};

struct TerminalLine {
public:
  std::vector<std::string> terminals;

  TerminalLine(const std::string &s);

  void show_string(std::ofstream &fout);
};

class Cyk {
private:
  struct Node {
    std::string parent;
    std::string left, right;
  };

  struct errors {
    struct alphabet : std::runtime_error {
      alphabet();
    };

    struct missing_arguments : std::runtime_error {
      missing_arguments();
    };

    struct wrong_mode : std::runtime_error {
        wrong_mode();
    };
  };

  TerminalLine mainString;
  Matrix mainMatrix;
  std::vector<Node> tree;
  std::map<std::pair<std::string, std::string>, std::set<std::string>> rules;

  void parse_line(std::string line);
  std::pair<int, std::string> read_word(std::string line, int index,
                                        char endWord);
  std::vector<std::string>
  vector_union(const std::vector<std::string> &first_cell,
               const std::vector<std::string> &second_cell);

  void build_tree(int row, int column, const std::string &parent);
  void show_tree(std::ofstream &fout);
  void show_rules(std::ofstream &fout);

public:
  Cyk(std::string s);

  void parser(std::ifstream &fin, const std::string &filename);
  void print_main_matrix(std::ofstream &fout);
  void algorithm(const std::string &filename, const std::string &mode);

  void check_troubles(int count_of_argument, std::string mode);
};

} // namespace cyk_algorithm

#endif