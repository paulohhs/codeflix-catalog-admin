from uuid import UUID

import pytest

from unittest.mock import create_autospec
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def mock_comedy_genre() -> Genre:
    return Genre(name="Comedy")


@pytest.fixture
def mock_drama_genre() -> Genre:
    return Genre(name="Drama")


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)


@pytest.fixture
def mock_genre_repository_with_data(
    mock_comedy_genre,
    mock_drama_genre,
) -> tuple[Genre, Genre, GenreRepository]:
    repository = create_autospec(GenreRepository)
    repository.list.return_value = [mock_comedy_genre, mock_drama_genre]

    return mock_comedy_genre, mock_drama_genre, repository



@pytest.fixture(scope="function")
def mock_genre_with_categories() -> callable:
    def make_mock(name: str, categories: set[UUID]) -> Genre:
        return Genre(
            name=name,
            categories=categories,
        )

    yield make_mock


@pytest.fixture
def mock_im_genre_repository() -> InMemoryGenreRepository:
    return InMemoryGenreRepository()


@pytest.fixture
def mock_im_genre_repository_with_data(
    mock_comedy_genre,
    mock_drama_genre,
) -> tuple[Genre, Genre, InMemoryGenreRepository]:
    repository = InMemoryGenreRepository(
        genres=[mock_comedy_genre, mock_drama_genre]
    )

    return mock_comedy_genre, mock_drama_genre, repository
