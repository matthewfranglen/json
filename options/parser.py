# This handles parsing both the incoming json data and the path

import json
import re

def parse_json(data):
    """
    Parses the data using the json library.
    No additional processing is done.
    """
    return json.loads(data)

def parse_arguments(data):
    """
    Parses the command line matching argument.
    Returns each argument in order as a tuple, indicating the type of operator as well as the usage of that operator.
    """

class ArgumentParser():
    """Parses each token in the argument string, returning it as a tuple with associated information"""

class ArgumentParserState():
    """Individual states deal with parsing specific types of arguments. This is the abstract superclass that defines what a state is."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def parse(data):
        """This will parse one token from the data and return the remaining data and the token as a two part tuple."""

class _EntryState(ArgumentParserState):
    """Determines the correct state to use to parse the token"""

    def parse(data):

class _StringState(ArgumentParserState):
    """Captures strings, where they start and end with the same quote character. Permits escaping with \\."""

    def parse(data):
        (string, _) = (quote, data) = (data[0], data[1:])
        escaped     = 0

        assert quote == '"' or quote == '"', 'invalid string quote'

        while data:
            (current, data)  = (data[0], data[1:])
            string          += current

            if not escaped and current == quote:
                return ((string, 'string'), data)

            escaped = not escaped and current == '\\'

        raise SyntaxError('Unterminated string, %s' % string)

class _NumberState(ArgumentParserState):
    """Captures numbers. Supports . and e"""

    def parse(data):
        pass

class _TokenState(ArgumentParserState):
    """Captures tokens wrapped in delimiters where those delimiters vary. Things like { this } and [ this ]."""
    _closers = { '{': '}', '[': ']' }

    def parse(data):
        (string, _) = (opener, data) = (data[0], data[1:])
        count       = 1
        
        assert opener in _closers, 'invalid token opener'
        closer = _closers[ opener ]

        while data:
            (current, data)  = (data[0], data[1:])
            string          += current

            if current == opener:
                count++
            elif current == closer:
                count--
                if count <= 0:
                    return ((string, 'token'), data)

        raise SyntaxError('Unterminated token, %s' % string)

class _OperatorState(ArgumentParserState):
    """Captures one of the operators defined in the README"""
    _operators = frozenset([ '==', '=', '>', '<', '~', '!', ':' ])

    def parse(data):
        (string, data) = (data[0], data[1:])

        assert string in _operators, 'invalid operator'

        while data and string + data[0] in _operators:
            string += data[0]
            data    = data[1:]
        
        return ((string, 'operator'), data)
