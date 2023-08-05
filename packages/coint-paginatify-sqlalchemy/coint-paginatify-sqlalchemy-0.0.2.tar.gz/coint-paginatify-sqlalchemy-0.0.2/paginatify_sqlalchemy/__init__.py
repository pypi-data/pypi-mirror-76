from typing import TypeVar, Callable

from paginatify import NavigationBase, Pagination, paginatify as _paginatify
from sqlalchemy.orm import Query


class QueryWrapper(object):
    def __init__(self, query):
        self.query = query

    def __len__(self):
        return self.query.count()

    def __getitem__(self, item):
        return self.query.__getitem__(item)


T = TypeVar('T')
U = TypeVar('U')


def paginatify(query: Query, page=1, per_page=10, per_nav=10, base: NavigationBase = NavigationBase.STANDARD,
               map_: Callable[[T], U] = lambda x: x) -> Pagination[U]:
    return _paginatify(QueryWrapper(query), page, per_page, per_nav, base, map_)
