from dataclasses import dataclass
from uuid import UUID

from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.use_cases.exceptions import GenreNotFound


class DeleteGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        genre = self.repository.get_by_id(id=input.id)

        if not genre:
            raise GenreNotFound("Genre not found")

        self.repository.delete(id=input.id)
