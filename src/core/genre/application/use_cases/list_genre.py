from dataclasses import dataclass
from uuid import UUID

from src.core.genre.domain.genre_repository import GenreRepository
from src.core._shared.application.list_response import ListOutput, ListOutputMeta, ListInput


@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]


class ListGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    @dataclass
    class Input(ListInput):
        pass

    @dataclass
    class Output(ListOutput[GenreOutput]):
        pass

    def execute(self, input: Input) -> Output:
        genres = self.repository.list()

        sorted_genres = sorted(
            [
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories,
                ) for genre in genres
            ],
            key=lambda genre: getattr(genre, input.order_by)
        )

        DEFAULT_PAGE_SIZE = 2
        page_offset = (input.current_page - 1) * DEFAULT_PAGE_SIZE
        genres_page = sorted_genres[page_offset:page_offset + DEFAULT_PAGE_SIZE]

        return self.Output(
            data=genres_page,
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=DEFAULT_PAGE_SIZE,
                total=len(sorted_genres)
            )
        )