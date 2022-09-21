from typing import List
from pyqurl.core import Query, QueryPagination, QuerySort
from pyqurl.operations import *
from pony.orm.core import desc


def str2bool(v):
  return str(v).lower() in ("yes", "true", "t", "1", "on")


class PonyORMHelper:

    @classmethod
    def apply_filters(cls, query, filters):
        if filters is None:
            return query

        for f in filters:
            if f.operation == EQUAL:
                query = query.filter(lambda x: getattr(x, f.prop) == f.value)

            elif f.operation == NOT_EQUAL:
                query = query.filter(lambda x: getattr(x, f.prop) != f.value)
                
            elif f.operation == CONTAINS:
                if isinstance(f.value, str):
                    query = query.filter(lambda x: f.value.lower() in getattr(x, f.prop).lower())
                else:
                    query = query.filter(lambda x: f.value in getattr(x, f.prop))

            elif f.operation == NOT_NULL:
                if str2bool(f.value):
                    query = query.filter(lambda x: getattr(x, f.prop) is not None)
                else:
                    query = query.filter(lambda x: getattr(x, f.prop) is None)

        return query    

    @classmethod
    def apply_pagination(cls, query, pagination: QueryPagination):
        if pagination is None:
            return query

        return query.limit(pagination.limit, offset=pagination.offset)

    @classmethod
    def apply_sorting(cls, query, sorts: List[QuerySort]):
        if sorts is None:
            return query

        for sort in sorts:
            query = query.order_by(lambda x: desc(getattr(x, sort.prop))) \
                if sort.descending else \
                    query.order_by(lambda x: getattr(x, sort.prop))

        return query

    @classmethod
    def apply_query(cls, pony_query, query: Query):
        if query is None:
            return pony_query

        filtered_query = cls.apply_filters(pony_query, query.filters)
        ordered_query = cls.apply_sorting(filtered_query, query.sort)
        paginated_query = cls.apply_pagination(ordered_query, query.pagination)
        return paginated_query