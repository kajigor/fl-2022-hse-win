#!/usr/bin/env bash

if [ $# -lt 1 ]; then
    echo "File with grammar was not provided"
    exit 0
fi

INPUT=$1 # name of file with grammar in txt

if ! [ -f "$INPUT" ]; then # check that file exists
    echo "$INPUT does not exist"
    exit 0
fi

FILE_NAME=$(echo "$INPUT" | sed -r -e 's/^(.+)\.txt$/\1/') # deleting ".txt"
LEXER_OUT="${INPUT}.out" # name of lexer output file with lextokens
touch "$LEXER_OUT"
ERR="stderr.txt" #errors
python3 executable_for_CNF/grammar_lexer.py "$INPUT" &> "$ERR" # executing lexer and redirecting errors to stderr.txt

if [ -s "$ERR" ]; then # check that grammar is valid
      cat "$ERR"
      echo "Incorrect input"
      exit 0
fi

CNF_GRAMMAR_OUT_MAIN="${FILE_NAME}_CNF.txt"  # file with grammar in CNF
CNF_GRAMMAR_OUT_OPT="${FILE_NAME}_CNF_step_by_step.txt" # every iteration of algorithm output (optional)
touch "$CNF_GRAMMAR_OUT_MAIN" "$CNF_GRAMMAR_OUT_OPT"
g++ executable_for_CNF/main.cpp executable_for_CNF/cnf.cpp -std=c++17 -o executable_for_CNF/main # compile
./executable_for_CNF/main "$LEXER_OUT" "$CNF_GRAMMAR_OUT_MAIN" "$CNF_GRAMMAR_OUT_OPT" #execute CNF algorithm

if [ $# -lt 4 ]; then
    echo "missing arguments"
    exit 0
fi

STRING_TO_THE_CYK=$2 # input in CYK algorithm
MODE=$3 #silent or show_steps
VIS_FILE=$4 # file, where must be out

if ! [ -f "$VIS_FILE" ]; then # check that file exists
    touch "$VIS_FILE"
fi

g++ executable_for_CYK/main.cpp executable_for_CYK/CYK.cpp -std=c++17 -o executable_for_CYK/main #compile
./executable_for_CYK/main "$CNF_GRAMMAR_OUT_MAIN" "$STRING_TO_THE_CYK" "$MODE" "$VIS_FILE"