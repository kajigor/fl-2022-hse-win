#!/usr/bin/env sh
INPUT=$1
FILENAME=$(echo "$INPUT" | sed -r -e 's/^(.+)\.txt$/\1/')
LEXEROUT="${INPUT}.out"
touch "$LEXEROUT"
python3 executable/grammar_lexer.py "$INPUT"
CNFGRAMMAROUT="${FILENAME}_CNF.txt"
touch "$CNFGRAMMAROUT"
g++ executable/main.cpp executable/cnf.cpp -std=c++17 -o executable/main
./executable/main "$LEXEROUT" "$CNFGRAMMAROUT"
