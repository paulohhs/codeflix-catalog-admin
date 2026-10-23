import uuid
import pytest

from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound


class TestCreateGenre:
    def test_create_genre_with_associated_categories(
        self,
        mock_im_genre_repository,
        mock_im_category_repository_with_data,
    ):
        (
            movie_category,
            documentary_category,
            category_repository
        ) = mock_im_category_repository_with_data

        use_case = CreateGenre(
            repository=mock_im_genre_repository,
            category_repository=category_repository,
        )
        input = CreateGenre.Input(
            name="Action",
            categories={movie_category.id, documentary_category.id}
        )

        output = use_case.execute(input=input)
        assert isinstance(output.id, uuid.UUID)

        saved_genre = mock_im_genre_repository.get_by_id(output.id)
        assert saved_genre.name == "Action"
        assert saved_genre.categories == {movie_category.id, documentary_category.id}
        assert saved_genre.is_active is True

    def test_create_genre_with_inexistent_categories_raise_an_error(
        self,
        mock_im_genre_repository,
        mock_im_category_repository,
    ):
        use_case = CreateGenre(
            repository=mock_im_genre_repository,
            category_repository=mock_im_category_repository
        )
        category_id = uuid.uuid4()
        input = CreateGenre.Input(
            name="Comedy",
            categories={category_id}
        )

        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input=input)

        assert str(category_id) in str(exc_info.value)

    def test_create_genre_without_categories(
        self,
        mock_im_genre_repository,
        mock_im_category_repository,
    ):
        use_case = CreateGenre(
            repository=mock_im_genre_repository,
            category_repository=mock_im_category_repository
        )
        input = CreateGenre.Input(name="Comedy")

        output = use_case.execute(input=input)

        assert isinstance(output.id, uuid.UUID)
        created_genre = mock_im_genre_repository.get_by_id(output.id)
        assert created_genre.name == "Comedy"
        assert created_genre.categories == set()
        assert created_genre.is_active
