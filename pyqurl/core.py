

from dataclasses import dataclass, field
import dataclasses
import re
from typing import Any, Dict, List, Union
from urllib.parse import parse_qs
from datetime import datetime

from pyqurl.operations import *
from pyqurl.helpers import str2bool
from pyqurl.exceptions import UnknownOperatorError


@dataclass
class QueryCriterion:
    prop: str
    operation: FilterOperation


@dataclass
class SingleValueQueryCriterion(QueryCriterion):
    value: Any


@dataclass
class ArrayValueQueryCriterion(QueryCriterion):
    value: List[Any]


@dataclass
class RangeValueQueryFilter(QueryCriterion):
    start: Any
    end: Any


@dataclass
class QuerySort:
    prop: str
    descending: bool


@dataclass
class QueryPagination:
    limit: int
    offset: Union[int, str]


@dataclass
class QueryFilter:
    criteria: List[QueryCriterion] = field(default_factory=list)
    sort: List[QuerySort] = field(default_factory=list)
    pagination: QueryPagination = None

    def clone(self):
        return QueryFilter(
            [dataclasses.replace(x) for x in self.criteria] if self.criteria else [],
            [dataclasses.replace(x) for x in self.sort] if self.sort else [],
            dataclasses.replace(self.pagination) if self.pagination else None
        )



QUERY_KEY_REGEX = r"(\w*)[\[]?(\w*)?[\]]?"
QUERY_SORT_REGEX = r"([-+])?(\w*)"

def create_query_from_string(q: str) -> QueryFilter:
    d = parse_qs(q)
    return create_query_from_dict(d)


def create_query_from_dict(d: Dict) -> QueryFilter:
    args = {**d}

    if offset := args.pop("offset", 0):
        offset = offset[0] if isinstance(offset, (list, tuple, )) else offset
        try:
            offset = int(offset)
        except ValueError:
            pass


    if limit := args.pop("limit", None):
        limit = int(limit[0] if isinstance(limit, (list, tuple, )) else limit)


    pagination = QueryPagination(limit, offset) if limit else None

    sort = create_sort_from_string(args.pop("sort", None))

    filters = create_filters_from_dict(args)

    return QueryFilter(filters, sort, pagination)


def parse_string_value(value: str) -> Any:
    if value is None or value.lower().strip() == "null":
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        pass

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value

def create_criterion(prop, op, value):

    if not isinstance(value, List):
        value = [value]

    if op in [IN, NOT_IN]:
        f = ArrayValueQueryCriterion(prop, op, value)

    elif op == NOT_NULL:
        f = SingleValueQueryCriterion(prop, op, str2bool(value[0]))

    elif op == RANGE:
        start, end = value if value is not None else (None, None, )
        f = RangeValueQueryFilter(prop, op, start=start, end=end)

    else:
        f = SingleValueQueryCriterion(prop, op, value[0])

    return f

def create_filters_from_dict(d: Dict):
    filters = []
    for key, value in d.items():
        if key is None or key.strip() == "":
            continue

        matches = re.search(QUERY_KEY_REGEX, key)
        prop, opvalue = matches.groups()

        if not opvalue:
            opvalue = EQUAL.value

        # Ensure value is a list
        if isinstance(value, List):
            value = ",".join(value).split(",")
        else:
            value = [value]

        # Try map every value to a number
        for i in range(len(value)):
            value[i] = parse_string_value(value[i])


        try:
            op = OPERATIONS_BY_VALUE[opvalue]
        except KeyError:
            raise UnknownOperatorError(opvalue)

        f = create_criterion(prop, op, value)

        filters.append(f)

    return filters

def create_sort_from_string(value: Union[str, List]):
    if value is None:
        return None
    r = []

    if isinstance(value, List):
        value = ",".join(value).split(",")
    else:
        value = str(value).split(",")

    for v in value:
        if not v:
            continue
        order, prop = re.search(QUERY_SORT_REGEX, v.strip()).groups()
        r.append(QuerySort(prop, order == "-"))
    return r





