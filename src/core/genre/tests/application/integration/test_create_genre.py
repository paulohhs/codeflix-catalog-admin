import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def category_repository(
    movie_category, documentary_category
) -> InMemoryCategoryRepository:
    return InMemoryCategoryRepository(
        categories=[movie_category, documentary_category]
    )


@pytest.fixture
def empty_category_repository() -> InMemoryCategoryRepository:
    return InMemoryCategoryRepository()


class TestCreateGenre:
    def test_create_genre_with_associated_categories(
        self,
        movie_category,
        documentary_category,
        category_repository,
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids={movie_category.id, documentary_category.id}
        )

        output = use_case.execute(input=input)
        assert isinstance(output.id, uuid.UUID)

        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre.name == "Action"
        assert saved_genre.categories == {movie_category.id, documentary_category.id}
        assert saved_genre.is_active is True

    def test_create_genre_with_inexistent_categories_raise_an_error(
        self,
        empty_category_repository,
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=empty_category_repository
        )
        category_id = uuid.uuid4()
        input = CreateGenre.Input(
            name="Comedy",
            category_ids={category_id}
        )

        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input=input)

        assert str(category_id) in str(exc_info.value)

    def test_create_genre_without_categories(
        self,
        empty_category_repository,
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=empty_category_repository
        )
        input = CreateGenre.Input(name="Comedy")

        output = use_case.execute(input=input)

        assert isinstance(output.id, uuid.UUID)
        created_genre = genre_repository.get_by_id(output.id)
        assert created_genre.name == "Comedy"
        assert created_genre.categories == set()
        assert created_genre.is_active
