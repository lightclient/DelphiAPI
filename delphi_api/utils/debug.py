def pretty_print(list):

    longest_key = 0
    longest_val = 0
    for el in list:
        longest_key = len(el[0]) if len(el[0]) > longest_key else longest_key
        longest_val = len(el[1]) if len(el[1]) > longest_val else longest_val

    for el in list:
        print( "+" + "-" * (longest_key + 2) + "+" + "-" * (longest_val + 2) + "+" )
        print( "| " + el[0] + " " * (longest_key - len(el[0])) + " | " + el[1] + " " * (longest_val - len(el[1])) + " |" )


    print( "+" + "-" * (longest_key + 2) + "+" + "-" * (longest_val + 2) + "+" )
