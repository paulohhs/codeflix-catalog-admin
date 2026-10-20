from dataclasses import dataclass, field
from uuid import UUID

from src.core.genre.application.use_cases.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.category.domain.category_repository import CategoryRepository


class CreateGenre:
    def __init__(self, repository: GenreRepository, category_repository: CategoryRepository):
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        name: str
        categories: set[UUID] = field(default_factory=set)
        is_active: bool = True

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input):
        categories = {category.id for category in self.category_repository.list()}

        if not input.categories.issubset(categories):
            raise RelatedCategoriesNotFound(
                f"Categories not found: {input.categories - categories}"
            )

        try:
            genre = Genre(
                name=input.name,
                is_active=input.is_active,
                categories=input.categories
            )
        except ValueError as e:
            raise InvalidGenre(e)

        self.repository.save(genre)

        return self.Output(id=genre.id)
        