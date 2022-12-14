import pytest

from pyqurl import create_query_from_string, create_query_from_dict
from pyqurl.exceptions import UnknownOperatorError
from pyqurl.operations import *


def test_single_explicit_equal_operator():
    query = create_query_from_string("name[eq]=gabriel")
    assert query.criteria[0].prop == "name"
    assert query.criteria[0].operation == EQUAL
    assert query.criteria[0].value == "gabriel"


def test_single_implicit_equal_operator():
    query = create_query_from_string("name=gabriel")
    assert query.criteria[0].prop == "name"
    assert query.criteria[0].operation == EQUAL
    assert query.criteria[0].value == "gabriel"


def test_multiple_equal_operators():
    query = create_query_from_string("name=john&surname=doe")

    assert query.criteria[0].prop == "name"
    assert query.criteria[0].operation == EQUAL
    assert query.criteria[0].value == "john"

    assert query.criteria[1].prop == "surname"
    assert query.criteria[1].operation == EQUAL
    assert query.criteria[1].value == "doe"

def test_query_without_value():
    query = create_query_from_string("name=")
    assert len(query.criteria) == 0

def test_query_without_prop():
    query = create_query_from_string("=value")
    assert len(query.criteria) == 0

def test_single_contains_operator():
    query = create_query_from_string("name[ct]=something")
    assert query.criteria[0].prop == "name"
    assert query.criteria[0].operation == CONTAINS
    assert query.criteria[0].value == "something"


def test_single_notnull_operator_should_be_true():
    query = create_query_from_string("deleted[nn]=true")
    assert query.criteria[0].prop == "deleted"
    assert query.criteria[0].operation == NOT_NULL
    assert query.criteria[0].value == True


def test_single_notnull_operator_should_be_false():
    query = create_query_from_string("deleted[nn]=false")
    assert query.criteria[0].prop == "deleted"
    assert query.criteria[0].operation == NOT_NULL
    assert query.criteria[0].value == False


def test_unknown_operator_should_raise_exception():
    with pytest.raises(UnknownOperatorError):
        create_query_from_string("abc[aaaaa]=abc")


def test_single_in_operator():
    query = create_query_from_string("color[in]=red,green,blue")
    assert query.criteria[0].prop == "color"
    assert query.criteria[0].operation == IN
    assert query.criteria[0].value == ["red", "green", "blue"]


def test_single_in_operator():
    query = create_query_from_string("year[rng]=1990,2010")
    assert query.criteria[0].prop == "year"
    assert query.criteria[0].operation == RANGE
    assert query.criteria[0].start == 1990
    assert query.criteria[0].end == 2010


def test_pagination():
    query = create_query_from_string("offset=20&limit=10")
    assert query.pagination is not None
    assert query.pagination.offset == 20
    assert query.pagination.limit == 10

def test_pagination_with_string_offset():
    query = create_query_from_string("offset=abc&limit=10")
    assert query.pagination is not None
    assert query.pagination.offset == "abc"
    assert query.pagination.limit == 10


def test_pagination_with_dict():
    query = create_query_from_dict({
        "offset": ["abc"],
        "limit": 10
    })
    assert query.pagination is not None
    assert query.pagination.offset == "abc"
    assert query.pagination.limit == 10


def test_sort_implicit_ascending():
    query = create_query_from_string("sort=id")
    assert query.sort is not None
    assert query.sort[0].prop == "id"
    assert query.sort[0].descending == False


def test_sort_explicit_ascending():
    query = create_query_from_string("sort=+id")
    assert query.sort is not None
    assert query.sort[0].prop == "id"
    assert query.sort[0].descending == False


def test_sort_descending():
    query = create_query_from_string("sort=-id")
    assert query.sort is not None
    assert query.sort[0].prop == "id"
    assert query.sort[0].descending == True

def test_sort_multiples():
    query = create_query_from_string("sort=id,name")
    assert query.sort is not None

    assert query.sort[0].prop == "id"
    assert query.sort[0].descending == False

    assert query.sort[1].prop == "name"
    assert query.sort[1].descending == False


def test_sort_descending():
    query = create_query_from_string("sort=-id,-name")
    assert query.sort is not None

    assert query.sort[0].prop == "id"
    assert query.sort[0].descending == True

    assert query.sort[1].prop == "name"
    assert query.sort[1].descending == True