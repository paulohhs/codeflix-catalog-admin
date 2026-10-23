import uuid
import pytest

from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre import Genre


class TestCreateGenre:
    def test_when_categories_do_not_exist_then_raise_related_categories_not_found(
        self,
        mock_category_repository,
        mock_genre_repository,
    ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository
        )
        category_id = uuid.uuid4()
        input = CreateGenre.Input(
            name="Comedy",
            categories={category_id}
        )

        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input=input)

        assert str(category_id) in str(exc_info.value)

    def test_when_created_genre_is_invalid_then_raise_invalid_genre(
        self,
        mock_category_repository_with_data,
        mock_genre_repository,
    ):
        movie_category, _, category_repository = mock_category_repository_with_data
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=category_repository
        )
        input = CreateGenre.Input(
            name="",
            categories={movie_category.id}
        )

        with pytest.raises(InvalidGenre, match="name cannot be empty"):
            use_case.execute(input=input)

    def test_when_created_genre_is_valid_and_categories_exist_then_save_genre(
        self,
        mock_category_repository_with_data,
        mock_genre_repository,
    ):
        (
            movie_category,
            documentary_category,
            category_repository
        ) = mock_category_repository_with_data
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=category_repository
        )
        input = CreateGenre.Input(
            name="Comedy",
            categories={movie_category.id, documentary_category.id}
        )

        output = use_case.execute(input=input)

        assert isinstance(output.id, uuid.UUID)
        mock_genre_repository.save.assert_called_once_with(
            Genre(
                id=output.id,
                name="Comedy",
                is_active=True,
                categories={movie_category.id, documentary_category.id}
            )
        )

    def test_create_genre_without_categories(
        self,
        mock_category_repository,
        mock_genre_repository,
    ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository
        )
        input = CreateGenre.Input(name="Comedy")

        output = use_case.execute(input=input)

        assert isinstance(output.id, uuid.UUID)
        mock_genre_repository.save.assert_called_once_with(
            Genre(
                id=output.id,
                name="Comedy",
                is_active=True,
                categories=set()
            )
        )
