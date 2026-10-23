from unittest.mock import create_autospec

import pytest

from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


@pytest.fixture(scope="function")
def mock_category() -> callable:
    def make_mock(name: str, description: str) -> Category:
        return Category(
            name=name,
            description=description,
        )

    yield make_mock


@pytest.fixture(scope="function")
def mock_movie_category() -> callable:
    def make_mock(name: str = "Movie Category") -> Category:
        return Category(
            name="Movie",
            description="Movie description",
        )

    yield make_mock


@pytest.fixture(scope="function")
def mock_documentary_category() -> callable:
    def make_mock(name: str = "Movie Category") -> Category:
        return Category(
            name="Documentary",
            description="Documentary description",
        )

    yield make_mock


@pytest.fixture()
def mock_category_repository() -> CategoryRepository:
    return create_autospec(CategoryRepository)


@pytest.fixture()
def mock_category_repository_with_data(
    mock_movie_category,
    mock_documentary_category,
) -> tuple[Category, Category, CategoryRepository]:
    movia_category = mock_movie_category()
    documentary_category = mock_documentary_category()
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movia_category, documentary_category]

    return movia_category, documentary_category, repository


@pytest.fixture
def mock_im_category_repository() -> InMemoryCategoryRepository:
    return InMemoryCategoryRepository()


@pytest.fixture
def mock_im_category_repository_with_data(
    mock_movie_category,
    mock_documentary_category,
) -> tuple[Category, Category, InMemoryCategoryRepository]:
    movia_category = mock_movie_category()
    documentary_category = mock_documentary_category()

    repository = InMemoryCategoryRepository(categories=[movia_category, documentary_category])

    return movia_category, documentary_category, repository
