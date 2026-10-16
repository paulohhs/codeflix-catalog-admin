from unittest.mock import create_autospec
import uuid

from src.core.genre.application.use_cases.list_genre import (
    ListGenre,
    GenreOutput,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class TestListGenre:
    def test_list_generes_with_associated_categories(self):
        genre_repository = create_autospec(GenreRepository)

        category_id_1 = uuid.uuid4()
        category_id_2 = uuid.uuid4()

        genre_terror = Genre(
            name="Terror",
            categories={category_id_1, category_id_2}
        )
        genre_comedy = Genre(name="Comedy")
        genre_repository.list.return_value = [genre_terror, genre_comedy]

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre_terror.id,
                    name=genre_terror.name,
                    is_active=genre_terror.is_active,
                    categories=genre_terror.categories,
                ),
                GenreOutput(
                    id=genre_comedy.id,
                    name=genre_comedy.name,
                    is_active=genre_comedy.is_active,
                    categories=genre_comedy.categories,
                )
            ]
        )

    def test_when_genre_doesnt_exist_return_empty_data(self):
        genre_repository = create_autospec(GenreRepository)
        genre_repository.list.return_value = []

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 0
        assert output == ListGenre.Output(data=[])
