#!/usr/bin/python
from options.parser  import parse_json, parse_arguments
from options.visitor import visit
from sys             import argv, stdin

def help():
    """
    Displays usage for this tool, with examples.
    """
    print """
json path

This prints all the values at path for the json provided. The json will come
from standard in.

The path allows you to specify what you are interested in. You do this by
specifying a list of operators that must successfully apply, in a manner
similar to css.

Some operators apply to the data passed in, while others apply to operators.
When a data operator depends on a specific type of data, such as looking up an
index in an array, that operator will reject all data that is not of that form.
"""

if __name__ == "__main__":
    json   = parse_json(stdin.read())
    rules  = parse_arguments(" ".join(argv[1:]))
    result = visit(rules, json)

    print result
