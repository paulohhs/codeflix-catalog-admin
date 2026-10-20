from unittest.mock import create_autospec
import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)


@pytest.fixture(scope="function")
def mock_category() -> callable:
    def make_mock(name: str) -> Category:
        return Category(name=name)

    yield make_mock


@pytest.fixture(scope="function")
def mock_category_repository() -> callable:
    def make_mock(categories: list[Category] | None = None) -> CategoryRepository:
        repository = create_autospec(CategoryRepository)

        if categories is not None and len(categories) >= 1:
            repository.list.return_value = categories

        return repository

    yield make_mock


class TestUpdateGenre:
    def test_when_genre_doesnt_exist_then_raise_genre_not_found(
        self,
        mock_genre_repository,
        mock_category_repository,
    ):
        mock_genre_repository.get_by_id.return_value = None

        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository
        )
        input = UpdateGenre.Input(
            id=uuid.uuid4(),
            name="Comedy",
            is_active=True,
            categories={uuid.uuid4(), uuid.uuid4()}
        )

        with pytest.raises(GenreNotFound):
            use_case.execute(input=input)

    def test_when_categories_associated_is_invalid_then_raise_related_categories_not_found(
        self,
        mock_category,
        mock_genre_repository,
        mock_category_repository,
    ):
        genre = Genre(name="Comedy")
        mock_genre_repository.get_by_id.return_value = genre

        movie_category = mock_category(name="Movie")
        documentary_category = mock_category(name="Documentary")
        category_repository = mock_category_repository(categories=[movie_category])

        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=category_repository,
        )
        input = UpdateGenre.Input(
            id=genre.id,
            name="Terror",
            is_active=True,
            categories={documentary_category.id}
        )
        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input=input)

    def test_when_attributes_is_invalid_then_raise_invalid_genre(
        self,
        mock_category,
        mock_genre_repository,
        mock_category_repository,
    ):
        movie_category = mock_category(name="Movie")
        documentary_category = mock_category(name="Documentary")
        category_repository = mock_category_repository(categories=[
            movie_category, documentary_category
        ])

        genre = Genre(name="Comedy")
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=category_repository
        )

        # Nome vazio não é permitido
        input = UpdateGenre.Input(
            id=genre.id,
            name="",
            is_active=True,
            categories={movie_category.id, documentary_category.id}
        )
        with pytest.raises(InvalidGenre):
            use_case.execute(input=input)

        # is_active deve ser do tipo bool
        input.name = "Terror"
        input.is_active = "Invalid type"
        with pytest.raises(InvalidGenre):
            use_case.execute(input=input)

    def test_attributes_is_valid_then_update_genre(
        self,
        mock_category,
        mock_genre_repository,
        mock_category_repository
    ):
        movie_category = mock_category(name="Movie")
        documentary_category = mock_category(name="Documentary")
        category_repository = mock_category_repository(categories=[
            movie_category, documentary_category
        ])
        
        genre = Genre(name="Comedy", is_active=False)
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=category_repository
        )

        input = UpdateGenre.Input(
            id=genre.id,
            name="Terror",
            is_active=True,
            categories={movie_category.id, documentary_category.id}
        )

        assert genre.name == "Comedy"
        assert genre.is_active is False
        assert genre.categories == set()
        
        use_case.execute(input=input)

        assert genre.name == "Terror"
        assert genre.is_active is True
        assert genre.categories == {movie_category.id, documentary_category.id}

    def test_when_updating_genre_all_categories_are_replaced(
        self,
        mock_category,
        mock_genre_repository,
        mock_category_repository,
    ):
        movie_category = mock_category(name="Movie")
        documentary_category = mock_category(name="Documentary")
        serie_category = mock_category("Serie")
        novel_category = mock_category(name="Novel")
        cartoon_category = mock_category(name="Cartoon")
        category_repository = mock_category_repository(categories=[
            movie_category,
            documentary_category,
            serie_category,
            novel_category,
            cartoon_category,
        ])
        
        genre = Genre(
            name="Comedy", 
            is_active=False,
            categories={
                movie_category.id, 
                serie_category.id, 
                documentary_category.id
            }
        )
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=category_repository
        )

        input = UpdateGenre.Input(
            id=genre.id,
            name="Terror",
            is_active=True,
            categories={novel_category.id, cartoon_category.id}
        )

        assert genre.name == "Comedy"
        assert genre.is_active is False
        assert genre.categories == {
            movie_category.id,
            documentary_category.id, 
            serie_category.id,
        }
        
        use_case.execute(input=input)

        assert genre.name == "Terror"
        assert genre.is_active is True
        assert genre.categories == {
            novel_category.id, 
            cartoon_category.id
        }