from abc import ABC
from dataclasses import dataclass, field
from typing import TypeVar, Generic


DEFAULT_PAGINATION_SIZE = 2


@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = DEFAULT_PAGINATION_SIZE
    total: int = 0


T = TypeVar("T")


@dataclass
class ListOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)
