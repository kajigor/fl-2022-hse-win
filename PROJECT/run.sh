#!/usr/bin/env sh
INPUT=$1 # name of file with grammar in txt
FILE_NAME=$(echo "$INPUT" | sed -r -e 's/^(.+)\.txt$/\1/') # deleting ".txt"
LEXER_OUT="${INPUT}.out" # name of lexer output file with lextokens
touch "$LEXER_OUT"
python3 executable/grammar_lexer.py "$INPUT" # execute lexer
CNF_GRAMMAR_OUT_MAIN="${FILE_NAME}_CNF.txt"  # file with grammar in CNF
CNF_GRAMMAR_OUT_OPT="${FILE_NAME}_CNF_step_by_step.txt" # every iteration of algorithm output (optional)
touch "$CNF_GRAMMAR_OUT_MAIN" "$CNF_GRAMMAR_OUT_OPT"
g++ executable/main.cpp executable/cnf.cpp -std=c++17 -o executable/main # compile
./executable/main "$LEXER_OUT" "$CNF_GRAMMAR_OUT_MAIN" "$CNF_GRAMMAR_OUT_OPT" #execute CNF algorithm
