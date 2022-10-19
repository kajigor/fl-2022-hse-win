#ifndef CNF_H_
#define CNF_H_

#include <string>
#include <vector>
#include <map>
#include <memory>
#include <regex>
#include <iostream>
#include <fstream>
#include <queue>
#include <cmath>
#include <set>

namespace cnf_grammar {

    enum class ObjectType {
        START_NON_TERM, NON_TERM, TERM, EPS, EQ, END
    };
    using rule_tp = std::vector<std::pair<ObjectType,int>>;

    struct NonTerm {
        std::string name;
        std::set<int> productions; // indexes of rules
        NonTerm (const std::string &s) : name(s) {}
    };

    class Grammar {
    private:
        bool hasEps = false; // may not contain epsilon
        int startID = 0;
        std::vector<std::vector<std::pair<ObjectType,int>>> rules; // one rule '('<S>')' consists of 3 elem-s
        std::vector<int> L; // for each rule its left non-term
        std::vector<NonTerm> nonTerms;
        std::vector<std::string> terms; // has no prod-s
        std::map<std::string, int> nonTermsID; // to get index by name
        std::map<std::string, int> termsID;

        std::string create_name(const std::string &s);
        int create_new_NonTerm(const std::string &nameTempl, const rule_tp& rule);
        void create_new_startNonTerm();
        void remove_non_single_terms();
        void remove_long_rules();
        void init_structures();
        void find_nullable();
        std::vector<int> add_rules(int left, const std::vector<rule_tp>& rulesToAdd);
        void remove_eps_rules();
        void remove_unit_rules();
    public:
        void convert_to_CNF();
        friend std::ifstream &operator>>(std::ifstream &is, Grammar &grammarToLoad);
        friend std::ofstream &operator<<(std::ofstream &out,
                                        const Grammar &grammarToPrint);
    };

}
#endif //CNF_H_
