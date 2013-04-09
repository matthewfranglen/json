# Represents the rule that the parser parses and the visitor uses

# Provides override for == and !=
# See: http://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
class CommonEqualityMixin(object):

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

class Rule(CommonEqualityMixin):
    """Represents a parsed rule"""
    TYPE_STRING   = 'string'
    TYPE_NUMBER   = 'number'
    TYPE_TOKEN    = 'token'
    TYPE_OPERATOR = 'operator'
    TYPES         = ( TYPE_STRING, TYPE_NUMBER, TYPE_TOKEN, TYPE_OPERATOR )

    def __init__(self, value, type):
        assert type in Rule.TYPES, 'Unknown type, %s' % type
        self.value = value
        self.type  = type
