Start non-terminal: expr
Non-terminals: ['expr', 'num']
Terminals: ['+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Rules: {

	 start --> [ expr ]

	 expr --> [ expr + num | expr - num | num ]

	 num --> [ num num | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ]

}
The grammar is in Chomsky Normal Form: False
