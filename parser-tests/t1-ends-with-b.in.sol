Start non-terminal: $S$
Non-terminals: {'$A$', '$S$'}
Terminals: {'#b#', '#a#'}
Rules: {

	$start$ --> [$S$]

	$S$ --> [#a# $S$  | #b# $A$]

	$A$ --> []

}
