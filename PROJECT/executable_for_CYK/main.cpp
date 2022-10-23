#include "CYK.hpp"

int main(int argc, char *argv[]) {
  /* first argument -- filename with CNF
   * second argument -- string to the CYK
   * third argument -- mode of out: show_steps, silent
   * forth argument -- file where must be ans
   */
  cyk_algorithm::Cyk mCYK(argv[2]);
  std::ifstream fin;
  mCYK.parser(fin, argv[1]);
  mCYK.check_troubles(argc, argv[3]);
  mCYK.algorithm(argv[4], argv[3]);
}
