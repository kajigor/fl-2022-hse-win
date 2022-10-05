Start non-terminal: $S$
Non-terminals: {'$S$'}
Terminals: {'#(#', '#eps#', '#)#'}
Rules: {
	$start$ --> [$S$]
	$S$ --> [#(# $S$ #)#]
	$S$ --> [$S$ $S$]

	$S$ --> [#eps#]

}
