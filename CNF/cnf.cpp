#include "cnf.hpp"

namespace cnf_grammar{


    std::map<std::string, ObjectType> dictionary = {{"START_NON_TERM", ObjectType::START_NON_TERM},
                                                    {"NON_TERM",ObjectType::NON_TERM},
                                                    {"TERM",ObjectType::TERM},
                                                    {"EPSILON",ObjectType::EPS},
                                                    {"EQ",ObjectType::EQ},
                                                    {"END",ObjectType::END}};

    std::ifstream &operator>>(std::ifstream &is,  Grammar &grammarToLoad) {
        std::smatch match;
        std::regex re(R"(LexToken\((.*?),('|")(.*?)('|"),\d+,\d+\))");
        std::string line;
        bool readingRight = false;
        int curNonTerm = -1;
        rule_tp curRule;

        while(std::getline(is , line)) {
            if(std::regex_search(line, match, re)) {
                std::string name = match[3];
                ObjectType type = dictionary[match[1]];
                switch (type) {
                    case ObjectType::EQ:
                        readingRight = true;
                        break;
                    case ObjectType::END: {
                        readingRight = false;
                        int idOfRule = grammarToLoad.rules.size();
                        grammarToLoad.rules.push_back(curRule);
                        grammarToLoad.nonTerms[curNonTerm].productions.push_back(idOfRule);
                        curRule.clear();
                        curNonTerm = -1;
                        break;
                    }
                    case ObjectType::TERM: {
                        if (!grammarToLoad.termsID.count(name)) {
                            grammarToLoad.termsID[name] = grammarToLoad.terms.size();
                            grammarToLoad.terms.push_back(name);
                        }
                        curRule.emplace_back(type, grammarToLoad.terms.size()-1);
                        break;
                    }
                    case ObjectType::START_NON_TERM:
                        if (!grammarToLoad.nonTermsID.count(name)) {
                            grammarToLoad.nonTermsID[name] = grammarToLoad.nonTerms.size();
                            grammarToLoad.startID = grammarToLoad.nonTerms.size();
                            grammarToLoad.nonTerms.emplace_back(name);
                        }
                    case ObjectType::NON_TERM: {
                        if (!grammarToLoad.nonTermsID.count(name)) {
                            grammarToLoad.nonTermsID[name] = grammarToLoad.nonTerms.size();
                            grammarToLoad.nonTerms.emplace_back(name);
                        }
                        int id = grammarToLoad.nonTermsID[name];
                        if (readingRight) {
                            curRule.emplace_back(ObjectType::NON_TERM, id);
                        } else {
                            curNonTerm = id;
                        }
                        break;
                    }
                    case ObjectType::EPS: {
                        if (!grammarToLoad.hasEps) {
                            grammarToLoad.hasEps = true;
                        }
                        curRule.emplace_back(type, -1);
                        break;
                    }
                }
            }
        }
        return is;
    }

    void Grammar::print() { //TODO: remake
        std::cout << '<' << nonTerms[startID].name << ">=";

        for(int i : nonTerms[startID].productions) {
            for (auto &[type, id]: rules[i]) {
                if(type == ObjectType::NON_TERM) {
                    std::cout << '<' << nonTerms[id].name << ">;\n";
                } else if (type == ObjectType::EPS) {
                    std::cout << '\'' << "E" << "\';\n";
                } else {
                    std::cout << '\'' << terms[id] << "\';\n";
                }
            }
        }

        for (int j = 0; j < nonTerms.size(); j++) {
            if(j == startID) continue;
            for(int i : nonTerms[j].productions) {
                std::cout << '<' << nonTerms[j].name << ">=";
                for (auto &[type, id]: rules[i]) {
                    if(type == ObjectType::NON_TERM) {
                        std::cout << '<' << nonTerms[id].name << ">";
                    } else if (type == ObjectType::EPS) {
                        std::cout << '\'' << "E" << "\'";
                    } else {
                        std::cout << '\'' << terms[id] << "\'";
                    }
                }
                std::cout << ";\n";
            }

        }
    }

    std::string Grammar::create_name(const std::string &s) {
        std::string name = s;
        for(int i = 0; ; i++){
            if(!nonTermsID.count(name + std::to_string(i))){
                name += std::to_string(i);
                break;
            }
        }
        return name;
    }

    int Grammar::create_new_NonTerm(const std::string &nameTempl, const rule_tp& rule) {
        std::string name = create_name(nameTempl);
        int nonTermId = nonTerms.size();
        int ruleId = rules.size();

        rules.push_back(rule);

        nonTermsID[name] = nonTermId;
        nonTerms.emplace_back(name);
        nonTerms[nonTermId].productions.push_back(ruleId);

        return nonTermId;
    }

    void Grammar::create_new_startNonTerm() {
        rule_tp r = {{ObjectType::NON_TERM, startID}};
        startID = create_new_NonTerm("S", r);
    }

    void Grammar::remove_non_single_terms() {
        std::map<int,int> createdNonTerms;

        for(int i = 0; i < rules.size(); i++) {
            if (rules[i].size() > 1) {
                for(int j = 0; j < rules[i].size(); j++) {
                    auto [type, id]  = rules[i][j];
                    if(type == ObjectType::TERM) {

                        if(!createdNonTerms.count(id)) {
                            rule_tp r = {{type, id}};
                            createdNonTerms[id] = create_new_NonTerm("T" , r);
                        }

                        rules[i][j].first = ObjectType::NON_TERM;
                        rules[i][j].second = createdNonTerms[id];
                    }
                }
            }
        }

    }

    void Grammar::remove_long_rules() {
        bool existLongRule = true;

        while(existLongRule) {
            existLongRule = false;

            for(int i = 0; i < rules.size(); i++) {
                if (rules[i].size() > 2) {
                    existLongRule = true;
                    rule_tp newRule;
                    while(rules[i].size() > 1) {
                        newRule.emplace_back(rules[i].back());
                        rules[i].pop_back();
                    }
                    std::reverse(newRule.begin(), newRule.end());
                    int IdN = create_new_NonTerm("H" , newRule);
                    rules[i].emplace_back(ObjectType::NON_TERM, IdN);
                }
            }
        }

    }

    void Grammar::remove_eps_rules() {

    }

    void Grammar::convert_to_CNF() {
        create_new_startNonTerm();
        remove_non_single_terms();
        remove_long_rules();
       // remove_eps_rules();
    }




}
