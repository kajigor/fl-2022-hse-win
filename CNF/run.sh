#!/usr/bin/env sh
INPUT=$1
FILENAME=$(echo "$INPUT" | sed -r -e 's/^(.+)\.txt$/\1/')
LEXEROUT="${INPUT}.out"
touch "$LEXEROUT"
python3 grammar_lexer.py "$INPUT"
CNFGRAMMAROUT="${FILENAME}_CNF.txt"
touch "$CNFGRAMMAROUT"
g++ main.cpp cnf.cpp -std=c++17 -o main
./main "$LEXEROUT" "$CNFGRAMMAROUT"
