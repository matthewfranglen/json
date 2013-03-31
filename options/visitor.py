# This visits the json data according to the path, returning all matching values.

import abc
import types

def visitor_factory(rule):
    """Creates the appropriate visitor for the rule provided"""

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
        self.do_visit(rules, node, last, parents)

        results = []
        for child in self.list_children(rules, node, last, parents):
            result = self.visit(rules, child, last, (node) + parents)
            if result:
                results = results + [result]
        return results

    def list_children(self, rules, node, last, parents):
        """This provides the list of children to visit"""
        # Only handle lists and dictionaries - json doesn't produce tuples or similar
        if type(node) is types.ListType:
            return [ node[child] for child in range(len(node)) if self.should_visit(rules, child, node, last, parents) ]
        if type(node) is types.DictionaryType:
            return [ node[child] for child in node.keys() if self.should_visit(rules, child, node, last, parents) ]
        return []

    def transition(self, rules, child, node, parents):
        """
        Creates the next visitor and starts it off at this point,
        or returns the node if no more rules exist.
        """
        if len(rules):
            visitor = visitor_factory(rules[0])
            return visitor.visit(rules[1:], child, node, (node) + parents)
        else:
            return child

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
        return node == last and child == self.index

class _CurrentVisitor(Visitor):
    """Visits the current node only"""
    pass

class _ChildVisitor(Visitor):
    """Visits the current children only"""
    pass

class _ComparisonVisitor(Visitor):
    """Boolean comparisons"""
    pass
