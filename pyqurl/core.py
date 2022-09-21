

from dataclasses import dataclass
import re
from typing import Any, Dict, List, Union
from urllib.parse import parse_qs
from datetime import datetime

from pyqurl.operations import *
from pyqurl.helpers import str2bool
from pyqurl.exceptions import UnknownOperatorError


@dataclass
class QueryFilter:
    prop: str
    operation: FilterOperation


@dataclass
class SingleValueQueryFilter(QueryFilter):
    value: Any


@dataclass
class ArrayValueQueryFilter(QueryFilter):
    value: List[Any]


@dataclass
class RangeValueQueryFilter(QueryFilter):
    start: Any
    end: Any


@dataclass
class QuerySort:
    prop: str
    descending: bool


@dataclass
class QueryPagination:
    limit: int
    offset: int


@dataclass
class Query:
    filters: List[QueryFilter]
    sort: List[QuerySort]
    pagination: QueryPagination


QUERY_KEY_REGEX = r"(\w*)[\[]?(\w*)?[\]]?"
QUERY_SORT_REGEX = r"([-+])?(\w*)"

def create_query_from_string(q: str) -> Query:
    d = parse_qs(q)
    return create_query_from_dict(d)


def create_query_from_dict(d: Dict) -> Query:
    args = {**d}

    offset = args.pop("offset", 0)
    limit = args.pop("limit", None)
    pagination = QueryPagination(int(limit), int(offset)) if limit else None

    sort = create_sort_from_string(args.pop("sort", None))
    
    filters = create_filters_from_dict(args)

    return Query(filters, sort, pagination)


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

        if op in [IN, NOT_IN]:
            f = ArrayValueQueryFilter(prop, op, value)

        elif op == NOT_NULL:
            f = SingleValueQueryFilter(prop, op, str2bool(value[0]))

        elif op == RANGE:
            start, end = value if value is not None else (None, None, )
            f = RangeValueQueryFilter(prop, op, start=start, end=end)

        else:           
            f = SingleValueQueryFilter(prop, op, value[0])
        
        filters.append(f)

    return filters

def create_sort_from_string(value: Union[str, List]):
    if value is None:
        return None
    r = []

    if isinstance(value, List):
        value = ",".join(value).split(",")
    else:
        value = [value]

    for v in value:
        if not v:
            continue
        order, prop = re.search(QUERY_SORT_REGEX, v.strip()).groups()
        r.append(QuerySort(prop, order == "-"))
    return r
    




