# cat file | cl_json path

This prints all the values at path for the json provided. The json will come from standard in as well as any specified files.

The path allows you to specify what you are interested in. You do this by specifying a list of operators that must successfully apply, in a manner similar to css.

Some operators apply to the data passed in, while others apply to operators. When a data operator depends on a specific type of data, such as looking up an index in an array, that operator will reject all data that is not of that form.

## OPERATORS:

### INDEXES

These operators apply to arrays and dicts and specify the value to return.

#### []  INDEX
This retrieves the specified index.

    [1] of [1, 2, 3] is 2
    [1] of {0: "zero", 1: "one"} is "one"

This can return the specified value from any eligible node. To restrict it to returning from just the node you tested, use the : operator. To restrict it to the direct child of the node you tested, use the > operator. See more about these below.

This does not have to be used to return a value from your expression. It can be used to restrict the traversal of the data structure.

### COMPARISONS
    
These operators apply to values directly. Whenever you specify them, you are testing any node which is valid up to this point. At the beginning, that will be all nodes. You specify them as:

    COMPARISON TEST

So:

    == "a"
    >  10

#### == EQUALS
This is compatible with any type and requires an exact, deep, match. You specify the data to match in python form, so:

    a string is "a string" or 'another string'
    a number is 1 or -0.5 or 5e10
    an array is [1, 2, 3]
    a dict is   {1: 2}

Arrays and tuples are tested exactly, so both order and content must match.

#### = PERMISSIVE EQUALS
This is compatible with any type and requires a more lax match than the regular equals operator. Types must match. String and number values must match. Arrays and dicts must contain all specified values, but can contain other values. The order does not have to match. This is designed for deeply testing data structures without being required to traverse them. For example:

    = { type: "person" } > ["name"]

This would return the name value of dicts that have a type of person.

#### > GREATER THAN
This is compatible with number and string types only. Performs a greater than test.

    "b" > "a"
    1   > 0.2

#### < LESS THAN
This is compatible with number and string types only. Performs a less than test.

    "a" < "b"
    0.2 < 1

#### ~ MATCHES
This is compatible with string types only. Performs a regular expression match.

    "a" ~ "."
 
### OPERATOR OPERATORS

#### ! NEGATE
Reverses the result of the operation that it applies to.

    "a" != "b"

#### : CURRENT
This forces the operator to be evaulated against the current value. This allows you to specify multiple conditions that a single value must pass, as well as testing and then returning indexes from an array or dict (remember that just passing the tests would otherwise make the entire array or dict be returned).

    = { type: "person" } : ["name"]

This returns the name value from the dict which has a type of person.

    = { type: "person" } : = { gender: "male" }

This returns the dicts that have a type of person and a gender of male (you could express this in a more compact way, but this is just an example).

#### > CHILD
This forces the operator to be evaluated only against the children of the current value. No further descent of the data structure is permitted. Given the structure:

    { type: "container", content: [ { type: "box", content: [ "food" ] } ] }

The following example expressions would all return "food":

    = { type: "box" } > [0]
    = { type: "container" } >> = { type: "box" } > [0]
    = { type: "container" } >>> [0]

