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

        genres_page = self.Output.paginate(
            objects=sorted_genres,
            per_page=input.per_page,
            current_page=input.current_page,
        )

        return self.Output(
            data=genres_page,
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=input.per_page,
                total=len(sorted_genres)
            )
        )