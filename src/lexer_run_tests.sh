#!/usr/bin/env bash

FLAG=0
for TESTFILE in "$@"; do
    OUTFILE="${TESTFILE}.out"
    EXPECTEDFILE="${TESTFILE}.expected"
    python3 lex.py $TESTFILE
    if ! cmp -s $OUTFILE $EXPECTEDFILE; then
        FLAG=1
	echo "Test failed: ${TESTFILE}"	
    fi
    rm $OUTFILE
done
if [ $FLAG -eq 0 ]; then
    echo "Tests passed"
fi
