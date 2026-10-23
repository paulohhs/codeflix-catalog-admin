from unittest.mock import create_autospec

import pytest

from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


@pytest.fixture(scope="function")
def mock_category() -> callable:
    def make_mock(name: str, description: str = "") -> Category:
        return Category(
            name=name,
            description=description,
        )

    yield make_mock


@pytest.fixture(scope="function")
def mock_movie_category() -> Category:
    return Category(
        name="Movie",
        description="Movie description",
    )


@pytest.fixture(scope="function")
def mock_documentary_category() -> Category:
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture()
def mock_category_repository() -> CategoryRepository:
    return create_autospec(CategoryRepository)


@pytest.fixture()
def mock_category_repository_with_data(
    mock_movie_category,
    mock_documentary_category,
) -> tuple[Category, Category, CategoryRepository]:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [
        mock_movie_category,
        mock_documentary_category
    ]

    return mock_movie_category, mock_documentary_category, repository


@pytest.fixture(scope="function")
def mock_category_repository_with_categories() -> callable:
    def make_mock(categories: list[Category] | None = None) -> CategoryRepository:
        repository = create_autospec(CategoryRepository)

        if categories is not None and len(categories) >= 1:
            repository.list.return_value = categories

        return repository

    yield make_mock


@pytest.fixture
def mock_im_category_repository() -> InMemoryCategoryRepository:
    return InMemoryCategoryRepository()


@pytest.fixture
def mock_im_category_repository_with_data(
    mock_movie_category,
    mock_documentary_category,
) -> tuple[Category, Category, InMemoryCategoryRepository]:
    repository = InMemoryCategoryRepository(
        categories=[mock_movie_category, mock_documentary_category]
    )

    return mock_movie_category, mock_documentary_category, repository
