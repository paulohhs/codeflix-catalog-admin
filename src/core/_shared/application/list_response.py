from abc import ABC
from dataclasses import dataclass, field
from typing import TypeVar, Generic


T = TypeVar("T")
DEFAULT_PAGINATION_SIZE = 2


@dataclass(kw_only=True)
class ListInput:
    order_by: str = "name"
    current_page: int = 1
    per_page: int = DEFAULT_PAGINATION_SIZE


@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = DEFAULT_PAGINATION_SIZE
    total: int = 0


@dataclass
class ListOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)

    @staticmethod
    def paginate(
        objects: list,
        per_page: int,
        current_page: int,
    ) -> list:
        page_offset = (current_page - 1) * per_page
        return objects[page_offset:page_offset + per_page]
