#include "CYK.hpp"

namespace cyk_algorithm {
void Cyk::print_main_matrix(std::ofstream &fout) {
  mainMatrix.print_matrix(fout);
  fout << '\n'
       << '\n'
       << "=============================================" << '\n';
}

void Matrix::insert_in_cell(int row, int column,
                            const std::vector<std::string> &new_cell) {
  int columnSize = 0;
  for (const std::string &non_terminal : new_cell) {
    columnSize += static_cast<int>(non_terminal.size()) + 2;
  }

  assert(row < matrix.size());
  assert(column < matrix[row].size());
  assert(column < columnsSize.size());

  columnsSize[column] = std::max(columnsSize[column], columnSize);
  matrix[row][column] = new_cell;
}

void Matrix::print_matrix(std::ofstream &fout) {
  for (auto row : matrix) {
    for (int i = 0; i < row.size(); ++i) {
      std::string cell;

      cell += "{ ";

      for (int token = 0; token < row[i].size(); token++) {
        cell += row[i][token];
        cell += token + 1 == row[i].size() ? "" : ", ";
      }

      for (int size_cell = static_cast<int>(cell.size());
           size_cell < columnsSize[i]; size_cell++) {
        cell += ' ';
      }

      fout << cell;
      fout << '}';
    }
    fout << '\n';
  }
}

int Matrix::get_size() const { return size; }

std::vector<std::string> Matrix::get_cell(int row, int column) {
  // assert(row >= 0);
  // assert(column >= 0);
  // assert(row < matrix.size());
  // assert(column < matrix.size());
  return matrix[row][column];
}

void Cyk::parser(std::ifstream &fin, const std::string &filename) {
  fin.open(filename);
  std::string line;
  while (getline(fin, line)) {
    parse_line(line);
  }
  fin.close();
}

void Cyk::parse_line(std::string line) {
  std::vector<std::string> tokens(3);
  int rule = 0;
  for (int i = 0; i < line.size(); i++) {
    if (line[i] == '<') {
      auto p = read_word(line, i + 1, '>');
      i = p.first;
      tokens[rule] = "<" + p.second + ">";
      rule++;
    }

    if (line[i] == '\'') {
      auto p = read_word(line, i + 1, '\'');
      i = p.first;
      tokens[rule] = "'" + p.second + "'";
      rule++;
    }
  }
  rules[{tokens[1], rule < 3 ? "-1" : tokens[2]}].insert(tokens[0]);
}

std::pair<int, std::string>
Cyk::read_word(std::string line, int index,
               char endWord) { // all words under rules
  std::string word;
  std::pair<int, std::string> result;
  while (line[index] != endWord ||
         (line[index - 1] == '\\' && line[index - 2] != '\\')) {
    word += line[index];
    index++;
  }
  result.first = index;
  result.second = word;
  return result;
}

void Cyk::algorithm(const std::string &filename, const std::string &mode) {
  // const auto rules_ = rules;

  std::ofstream fout;
  fout.open(filename);

  mainString.show_string(fout);

  for (int diagonal = 0; diagonal < mainMatrix.get_size(); diagonal++) {

    for (int i = 0, j = diagonal;
         i < mainMatrix.get_size() && j < mainMatrix.get_size(); i++, j++) {
      std::vector<std::string> newCell;

      int dp = diagonal;

      if (dp == 0) {
        std::pair<std::string, std::string> pp = {mainString.terminals[i],
                                                  "-1"};

        assert(rules.find(pp) != rules.end());

        for (const auto &rule : rules[pp]) {
          newCell.push_back(rule);
        }
      } else {
        while (dp > 0) {
          std::vector<std::string> result_of_union =
              vector_union(mainMatrix.get_cell(i, j - dp),
                           mainMatrix.get_cell(i + (diagonal - dp + 1), j));

          std::set<std::string> without_duplicate;

          for (const auto &token : result_of_union) {
            without_duplicate.insert(token);
          }

          for (const auto &token : newCell) {
            without_duplicate.insert(token);
          }

          newCell.clear();

          for (const auto &token : without_duplicate) {
            newCell.push_back(token);
          }

          dp--;
        }
      }

      mainMatrix.insert_in_cell(i, j, newCell);

      if (mode == "show_steps") {
        print_main_matrix(fout);
      }
    }
  }

  if (mode != "show_steps") {
    print_main_matrix(fout);
  }

  bool final_check = false;
  for (auto token : mainMatrix.get_cell(0, mainMatrix.get_size() - 1)) {
    if (token == "<S>") {
      final_check = true;
    }
  }

  fout << (final_check ? "Possible string\n" : "Impossible string\n");

  if (final_check) {
    build_tree(0, mainMatrix.get_size() - 1, "<S>");
    show_tree(fout);
    fout << '\n';
  }

  fout.close();
}

std::vector<std::string>
Cyk::vector_union(const std::vector<std::string> &first_cell,
                  const std::vector<std::string> &second_cell) {
  std::vector<std::string> answer;
  std::set<std::string> temp_result;

  for (auto token_from_first : first_cell) {
    std::pair<std::string, std::string> rule;
    if (token_from_first[0] == '\'') {

      rule.first = token_from_first;
      rule.second = "-1";

      if (!rules[rule].empty()) {

        for (const auto &non_terminal : rules[rule]) {
          temp_result.insert(non_terminal);
        }
      }

    } else {
      for (const auto &token_from_second : second_cell) {
        rule.first = token_from_first;
        rule.second = token_from_second;

        if (!rules[rule].empty()) {

          for (const auto &non_terminal : rules[rule]) {
            temp_result.insert(non_terminal);
          }
        }
      }
    }
  }

  for (const auto &rule : temp_result) {
    answer.push_back(rule);
  }

  return answer;
}

void Cyk::build_tree(int row, int column, const std::string &parent) {
  int diagonal = column - row;

  int dp = diagonal;

  if (diagonal == 0) {
    tree.push_back({parent, mainString.terminals[row], "-1"});
  } else {
    bool broke = false;
    std::string fst, snd;

    while (dp > 0) {
      for (auto token1 : mainMatrix.get_cell(row, column - dp)) {
        for (auto token2 :
             mainMatrix.get_cell(row + (diagonal - dp + 1), column)) {

          if (rules[{token1, token2}].find(parent) !=
              rules[{token1, token2}].end()) {
            fst = token1;
            snd = token2;
            broke = true;
          }
        }

        if (broke) {
          break;
        }
      }
      if (broke) {
        break;
      }
      dp--;
    }

    tree.push_back({parent, fst, snd});
    if (dp > 0) {
      assert(row >= 0 && row < mainMatrix.get_size());
      assert(column - row >= 0 && column - row < mainMatrix.get_size());
      assert(row + (diagonal - dp + 1) >= 0 &&
             row + (diagonal - dp + 1) < mainMatrix.get_size());
      assert(column >= 0 && column < mainMatrix.get_size());
      build_tree(row, column - dp, fst);
      build_tree(row + (diagonal - dp + 1), column, snd);
    }
  }
}

void Cyk::show_tree(std::ofstream &fout) {
  fout << "TREE:\n";
  for (const auto &node : tree) {
    fout << node.parent << " ---> (" << node.left << ", " << node.right
         << ")\n";
  }
}

void Cyk::show_rules(std::ofstream &fout) {
  for (auto [pt, st] : rules) {
    fout << pt.first << ' ' << pt.second << " ====== ";
    for (const auto &nonterm : st) {
      fout << nonterm << ' ';
    }
    fout << '\n';
  }
}

void Cyk::check_troubles(int count_of_argument, std::string mode) {

  if (count_of_argument < 4) {
    throw errors::missing_arguments();
  }

  bool all_in_alphabet = true;
  for (auto term: mainString.terminals){
      if (rules[{term, "-1"}].empty()){
          all_in_alphabet = false;
          break;
      }
  }

  if (!all_in_alphabet){
      throw errors::alphabet();
  }

  if (mode != "silent" && mode != "show_steps"){
      throw errors::wrong_mode();
  }

}

Cyk::Cyk(std::string s)
    : mainString(s), mainMatrix(mainString.terminals.size()) {}

TerminalLine::TerminalLine(const std::string &s) {
  bool openTerminal = false;
  bool openShielding = false;
  std::string word;

  for (char symbol : s) { // да-да я слышал про switch-case, и что?

    if (openShielding) {
      word += symbol;
      openShielding = false;
    } else {

      if (symbol == '\\') {
        openShielding = true;
        word += symbol;
      } else if (symbol == '\'') {
        if (openTerminal) {
          word += symbol;
          openTerminal = false;
          terminals.push_back(word);
          word = "";
        } else {
          openTerminal = true;
          word += symbol;
        }
      } else if (symbol == 'E') {
        continue;
      } else {
        word += symbol;
      }
    }
  }
}

void TerminalLine::show_string(std::ofstream &fout) {
  for (const auto& term: terminals){
    fout << term;
  }
  fout << '\n' << '\n';
}

    Cyk::errors::alphabet::alphabet()
    : std::runtime_error("unidentified characters") {}

Cyk::errors::missing_arguments::missing_arguments()
    : std::runtime_error("missing arguments") {}

    Cyk::errors::wrong_mode::wrong_mode() : std::runtime_error("Wrong mode: it must be show_steps or silent"){}
} // namespace cyk_algorithm