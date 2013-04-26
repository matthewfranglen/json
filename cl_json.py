#!/usr/bin/python
from options.parser  import parse_json, parse_arguments
from options.visitor import visit
from sys             import argv, stdin

def help():
    """
    Displays usage for this tool, with examples.
    """
    print """
cat file | json path

This prints all the values at path for the json provided. The json will come
from standard in.

See the README.md for syntax and examples.
"""

if __name__ == "__main__":
    if len(argv) < 2:
        help()
    else:
        json   = parse_json(stdin.read())
        rules  = parse_arguments(" ".join(argv[1:]))
        result = visit(rules, json)

        print result
