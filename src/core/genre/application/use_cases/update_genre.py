from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.use_cases.exceptions import (
    GenreNotFound, 
    InvalidGenre, 
    RelatedCategoriesNotFound
)


class UpdateGenre:
    def __init__(
        self, 
        repository: GenreRepository, 
        category_repository: CategoryRepository,
    ):
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        id: UUID
        name: str
        is_active: bool
        category_ids: set[UUID]

    def execute(self, input: Input) -> None:
        genre = self.repository.get_by_id(id=input.id)

        if not genre:
            raise GenreNotFound("Genre not found")

        category_ids = {category.id for category in self.category_repository.list()}
        
        if not input.category_ids.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories not found: {input.category_ids - category_ids}"
            )

        try:
            genre.change_name(name=input.name)
            genre.categories = input.category_ids

            if not isinstance(input.is_active, bool):
                raise ValueError("is_active must be True or False")

            if input.is_active:
                genre.activate()

            if not input.is_active:
                genre.deactivate

        except ValueError as e:
            raise InvalidGenre(e)

        self.repository.update(genre=genre)
