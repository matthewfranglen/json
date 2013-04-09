# This visits the json data according to the path, returning all matching values.

import abc
import types
import re

from rule import Rule

def visit(rules, node):
    """Visits the node according to the provided rules, returning the matches."""
    (visitor, rules) = visitor_factory(rules)
    return visitor.visit(rules, node, node, ())

class Visitor():
    """Implements the visitor code, which can be completed by a specific subclass."""
    __metaclass__ = abc.ABCMeta

    def visit(self, rules, node, last=None, parents=()):
        """
        This handles visiting the current nodes and any appropriate children.
        Arguments:
            rules   - a list of conditions which must be followed.
            node    - the current node being considered.
            last    - the node that triggered the last rule change (i.e. the last accepted node)
            parents - the list of parent nodes, all the way to the root.
        """
        node_value   = [ self.do_visit(rules, node, last, parents) ]
        child_values = [ self.visit(rules, child, last, (node,) + parents) for child in self.list_children(rules, node, last, parents) ]

        # Combine lists and flatten
        return [ item for list in node_value + child_values if list is not None
                      for item in list ]

    def list_children(self, rules, node, last, parents):
        """This provides the list of children to visit"""
        # Only handle lists and dictionaries - json doesn't produce tuples or similar
        if type(node) is types.ListType:
            return [ node[child] for child in range(len(node)) if self.should_visit(rules, child, node, last, parents) ]
        if type(node) is types.DictionaryType:
            return [ node[child] for child in node.keys()      if self.should_visit(rules, child, node, last, parents) ]
        return []

    def transition(self, rules, node, parents):
        """
        Creates the next visitor and starts it off at this point,
        or returns the node if no more rules exist.
        """
        if len(rules):
            (visitor, rules) = visitor_factory(rules)
            return visitor.visit(rules, node, node, parents)
        else:
            return [ node ]

    @abc.abstractmethod
    def should_visit(self, rules, child, node, last, parents):
        """This indicates if the node under consideration should be visited at all"""
        pass

    @abc.abstractmethod
    def do_visit(self, rules, node, last, parents):
        """This performs any required actions before the children are visited"""
        pass

class _IndexVisitor(Visitor):
    """Visits a specific index of the child"""
    
    def __init__(self, index):
        self.index = index

    def should_visit(self, rules, child, node, last, parents):
        return node == last and str(child) == str(self.index) # could be a dict key or an array index, but str covers both

    def do_visit(self, rules, node, last, parents):
        if len(parents) and parents[0] is last:
            return self.transition(rules, node, parents)

class _CurrentVisitor(Visitor):
    """Visits the current node only"""

    def should_visit(self, rules, child, node, last, parents):
        return 0
    def do_visit(self, rules, node, last, parents):
        return self.transition(self, rules, node, parents)

class _ChildVisitor(Visitor):
    """Visits the current children only"""

    def should_visit(self, rules, child, node, last, parents):
        return node == last

    def do_visit(self, rules, node, last, parents):
        if len(parents) and parents[0] == last:
            return self.transition(self, rules, node, parents)

class _ComparisonVisitor(Visitor):
    """Boolean comparisons"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, token):
        self.token = token

    @abc.abstractmethod
    def matches(self, node, token):
        pass

    def should_visit(self, rules, child, node, last, parents):
        return 0

    def do_visit(self, rules, node, last, parents):
        if self.matches(node, rules[0], self.token):
            return self.transition(self, rules, node, parents)

class _EqualsVisitor(_ComparisonVisitor):
    """Absolute Equality"""

    def matches(self, node, token):
        if type(node) == type(token):
            if type(node) == types.ListType:
                return self.list_matches(node, token)
            if type(node) == types.DictionaryType:
                return self.dict_matches(node, token)
            return node == token
        return 0

    def list_matches(self, node, token):
        if len(node) == len(token):
            return not len([ 'fail' for (n, t) in zip(node, token) if not self.matches(n, t) ])
        return 0

    def dict_matches(self, node, token):
        if len(node) == len(token):
            return not len([ 'fail' for k in node.keys() if k not in token or not self.matches(node[k], token[k]) ])
        return 0

class _PermissiveEqualsVisitor(_ComparisonVisitor):
    """Permissive Equality"""

class _GreaterThanVisitor(_ComparisonVisitor):
    """>"""
    def matches(self, node, token):
        return type(node) in (types.StringTypes, types.FloatType, types.IntType, types.LongType) and node > token

class _LessThanVisitor(_ComparisonVisitor):
    """<"""
    def matches(self, node, token):
        return type(node) in (types.StringTypes, types.FloatType, types.IntType, types.LongType) and node < token

class _MatchesVisitor(_ComparisonVisitor):
    """Regular Expression Match"""
    def matches(self, node, token):
        return type(node) == types.StringTypes and re.matches(node, token)

class _NegateVisitor(_ComparisonVisitor):
    """Wraps another comparison and negates it"""
    def __init__(self, comparison):
        self.comparison = comparison

    def matches(self, node, token):
        return not self.comparison.matches(node, token)

visitor_map = {
        '==': _EqualsVisitor,
        '=': _PermissiveEqualsVisitor,
        '<': _LessThanVisitor,
        '~': _MatchesVisitor,
    }

def visitor_factory(rules):
    """Creates the appropriate visitor for the rules provided"""
    assert len(rules), 'Operators terminate early'

    rule = rules[0]

    if rule.type == Rule.TYPE_TOKEN:
        return (_IndexVisitor(rule.value), rules[1:])
    elif rule.type == Rule.TYPE_OPERATOR:
        assert len(rules) > 1, 'Missing argument for operator %s' % rule.value

        if rule.value == '>':
            if not len(rules) or rules[1].type in (Rule.TYPE_OPERATOR, Rule.TYPE_TOKEN):
                return (_ChildVisitor(), rules[1:])
            else:
                return (_GreaterThanVisitor(rules[1].value), rules[2:])
        if rule[0] == '!':
            (condition, rules) = visitor_factory(rules[1:])
            return (_NegateVisitor(condition), rules)
        if rule in visitor_map:
            return (visitor_map[rule.value](rules[1].value), rules[2:])
        raise AssertionError('Unknown operator found, %s' % rule.value)
    else:
        raise AssertionError('Non operator found where operator expected')

