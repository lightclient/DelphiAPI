function pretty_print(list) {

	// Stringify everything
	for (var i = 0; i < list.length; i++) {
		list[i][0] = Object.is(list[i][0], undefined) ? "undefined" : list[i][0].toString()
		list[i][1] = Object.is(list[i][1], undefined) ? "undefined" : list[i][1].toString()
	}

	// Find longest key and value
	var longest_key = 0, longest_val = 0
	for ( var element of list ) {
		longest_key = element[0].length > longest_key ? element[0].length : longest_key
		longest_val = element[1].length > longest_val ? element[1].length : longest_val
	}

	// Print elements
	for (var element of list) {
		console.log( "+" + "-".repeat(longest_key + 2) + "+" + "-".repeat(longest_val + 2) + "+" )
		console.log("| " + element[0] + " ".repeat(longest_key - element[0].length) + " | " + element[1] + " ".repeat(longest_val - element[1].length) + " |")
	}

	// Print last line
	console.log( "+" + "-".repeat(longest_key + 2) + "+" + "-".repeat(longest_val + 2) + "+" )
}

exports.pretty_print = pretty_print
