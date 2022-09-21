from dataclasses import dataclass


@dataclass
class FilterOperation:
    value: str    


CONTAINS = FilterOperation("ct")
GREATER_THAN = FilterOperation("gt")
GREATER_THAN_OR_EQUAL = FilterOperation("gte")
LESSER_THAN = FilterOperation("lt"  )
LESSER_THAN_OR_EQUAL = FilterOperation("lte")
EQUAL = FilterOperation("eq")
NOT_EQUAL = FilterOperation("neq")
IN = FilterOperation("in")
NOT_IN = FilterOperation("nin")
RANGE = FilterOperation("rng")
NOT_NULL = FilterOperation("nn")


OPERATIONS = [
    CONTAINS,
    GREATER_THAN,
    GREATER_THAN_OR_EQUAL,
    LESSER_THAN,
    LESSER_THAN_OR_EQUAL,
    EQUAL,
    NOT_EQUAL,
    IN,
    NOT_IN,
    RANGE,
    NOT_NULL,
]


OPERATIONS_BY_VALUE = { o.value: o for o in OPERATIONS }
