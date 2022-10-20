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
                        grammarToLoad.L.push_back(curNonTerm);
                        grammarToLoad.nonTerms[curNonTerm].productions.insert(idOfRule);
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

    std::ofstream &operator<<(std::ofstream &out, const Grammar &grammarToPrint) {
        int startID = grammarToPrint.startID;

        for(int i : grammarToPrint.nonTerms[startID].productions) {
            out << '<' << grammarToPrint.nonTerms[startID].name << ">=";
            for (auto &[type, id]: grammarToPrint.rules[i]) {
                if(type == ObjectType::NON_TERM) {
                    out << '<' << grammarToPrint.nonTerms[id].name << ">";
                } else if (type == ObjectType::EPS) {
                    out << '\'' << "E" << "\'";
                } else {
                    out << '\'' << grammarToPrint.terms[id] << "\'";
                }
            }
            out << ";\n";
        }

        for (int j = 0; j < grammarToPrint.nonTerms.size(); j++) {
            if(j == startID) continue;
            for(int i : grammarToPrint.nonTerms[j].productions) {
                out << '<' << grammarToPrint.nonTerms[j].name << ">=";
                for (auto &[type, id]: grammarToPrint.rules[i]) {
                    if(type == ObjectType::NON_TERM) {
                        out << '<' << grammarToPrint.nonTerms[id].name << ">";
                    } else if (type == ObjectType::EPS) {
                        out << '\'' << "E" << "\'";
                    } else {
                        out << '\'' << grammarToPrint.terms[id] << "\'";
                    }
                }
                out << ";\n";
            }
        }

        return out;
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
        L.push_back(nonTermId);

        nonTermsID[name] = nonTermId;
        nonTerms.emplace_back(name);
        nonTerms[nonTermId].productions.insert(ruleId);

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

    namespace {
        std::vector<int> isEpsilon; // mark if non-term is nullable
        std::vector<std::vector<int>> concernedRules; // list of rules, where non-term is in right
        std::vector<int> counter; // for each rule count non-terms that are not marked yet
        std::queue<int> Q; // marked but not handled non-terms
    }

    void Grammar::init_structures() {
        std::size_t n  = nonTerms.size();
        isEpsilon.resize(n,0);
        concernedRules.resize(n);
        counter.resize(rules.size());

        for(int i = 0; i < rules.size(); i++) {
            int count = 0;
            for(const auto & [type, id] : rules[i]) {
                if(type == ObjectType::NON_TERM || type == ObjectType::START_NON_TERM) {
                    concernedRules[id].push_back(i);
                }
                if(type != ObjectType::EPS)
                    count ++ ;
            }
            counter[i] = count;
            if(!count) {
                Q.push(L[i]);
                isEpsilon[L[i]] = 1;
            }
        }

    }

    void Grammar::find_nullable(){
        init_structures();

        while(!Q.empty()){ // finding nullable non-terms
            int curNTerm = Q.front();
            Q.pop();
            for(int rule : concernedRules[curNTerm]) {
                counter[rule]--;
                if(!counter[rule]) {
                    Q.push(L[rule]);
                    isEpsilon[L[rule]] = 1;
                }
            }
        }
    }

    std::vector<rule_tp> generate_subsets(const rule_tp &rule, const std::vector<int> pos){
        std::vector<rule_tp> res;
        int n = pos.size();
        int count = std::pow(2,n) - 1; // last one with all included we already have
        int snum = 0;
        while(snum < count){
            rule_tp newRule;
            std::set<int> included;

            for(int i = 0; i < n; ++i){
                if((snum&(1<<i)) != 0){
                    included.insert(i);
                }
            }

            int posI = 0;
            for(int j = 0; j < rule.size(); j++) {
                if(posI > pos.size() || pos[posI] != j) { // we are after pos end or we are not in pos
                    newRule.push_back(rule[j]);
                } else if (pos[posI] == j) { // we are in pos
                    if (included.count(j)) { // we are included
                        newRule.push_back(rule[j]);
                    }
                    posI ++;
                }
            }

            if(!newRule.empty()) {
                res.push_back(newRule);
            }
            ++snum;
        }

        return res;
    }

    std::vector<int> Grammar::add_rules(int left, const std::vector<rule_tp>& rulesToAdd) {
        std::vector<int> result; // indexes of new rules
        for(auto r : rulesToAdd) {
            result.push_back(rules.size());
            rules.push_back(r);
            L[rules.size()] = left;
        }
        return result;
    }

    void Grammar::remove_eps_rules() {
        if( !hasEps ) return;

        find_nullable();

        for(int h = 0; h < nonTerms.size(); h++) {
            auto &A = nonTerms[h];
            std::vector<int> newRules; // id-s of new rules added

            for(int i : A.productions){
                auto rule = rules[i];
                std::vector<int> pos;

                for(int j = 0 ; j < rule.size(); j++) { // pos <- positions of nullable nTerms in rule
                    auto [tp, id] = rule[j];
                    if(tp == ObjectType::NON_TERM && isEpsilon[id]) {
                        pos.push_back(j);
                    }
                }

                if(pos.empty()) continue;
                std::vector<rule_tp> addRules = generate_subsets(rule, pos);
                std::vector<int> addedRulesIds = add_rules(h, addRules);
                for(auto rInd : addedRulesIds){
                    newRules.push_back(rInd);
                }
            }

            for(auto ind : newRules) {
                A.productions.insert(ind);
            }
        }


        if(isEpsilon[startID]) { // add eps to start
            rule_tp r = {{ObjectType::EPS, -1}};
            int ruleInd = rules.size();
            rules.push_back(r);
            L.push_back(startID);
            nonTerms[startID].productions.insert(ruleInd);
        }

        for(int i = 0; i < nonTerms.size(); i++){ //remove eps rules
            if( i == startID)
                continue;
            NonTerm &curNTerm = nonTerms[i];
            std::vector<int> to_remove;
            for(auto it : curNTerm.productions) {
                if(rules[it] == rule_tp {{ObjectType::EPS, -1}}) {
                    to_remove.push_back(it);
                }
            }
            for(auto it : to_remove) {
                curNTerm.productions.erase(it);
            }
        }
    }

    void Grammar::remove_unit_rules() {
        bool existsUnitRule = true;

        while (existsUnitRule) {
            existsUnitRule = false;

            for (int i = 0; i < nonTerms.size(); i++) {
                NonTerm &curNTerm = nonTerms[i];
                std::vector<int> to_remove;
                std::vector<int> nTermsIDs;

                for (auto it: curNTerm.productions) {
                    if (rules[it].size() == 1 && rules[it][0].first == ObjectType::NON_TERM) {
                        existsUnitRule = true;
                        nTermsIDs.push_back(rules[it][0].second);
                        to_remove.push_back(it);
                    }
                }

                for (auto it: to_remove) {
                    curNTerm.productions.erase(it);
                }

                for (int id: nTermsIDs) {
                    for (int r: nonTerms[id].productions) {
                        rule_tp rule = rules[r];
                        int ruleId = rules.size();
                        rules.push_back(rule);
                        L.push_back(i);
                        curNTerm.productions.insert(ruleId);
                    }
                }

            }
        }

    }

    void Grammar::convert_to_CNF() {
        create_new_startNonTerm();
        remove_non_single_terms();
        remove_long_rules();
        remove_eps_rules();
        remove_unit_rules();
//        remove_non_generating();
    }




}
