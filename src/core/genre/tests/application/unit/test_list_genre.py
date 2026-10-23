import uuid
import pytest

from src.core.genre.application.use_cases.list_genre import (
    ListGenre,
    GenreOutput,
)
from src.core.genre.domain.genre import Genre
from src.core._shared.application.list_response import ListOutputMeta


class TestListGenre:
    def test_list_generes_with_associated_categories(
        self,
        mock_genre_repository,
    ):
        category_id_1 = uuid.uuid4()
        category_id_2 = uuid.uuid4()

        genre_terror = Genre(
            name="Terror",
            categories={category_id_1, category_id_2}
        )
        genre_comedy = Genre(name="Comedy")
        mock_genre_repository.list.return_value = [genre_terror, genre_comedy]

        use_case = ListGenre(repository=mock_genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre_comedy.id,
                    name=genre_comedy.name,
                    is_active=genre_comedy.is_active,
                    categories=genre_comedy.categories,
                ),
                GenreOutput(
                    id=genre_terror.id,
                    name=genre_terror.name,
                    is_active=genre_terror.is_active,
                    categories=genre_terror.categories,
                )
            ],
            meta = ListOutputMeta(
                current_page=1,
                per_page=2,
                total=2,
            )
        )

    @pytest.mark.parametrize(
        "current_page",
        [1, 2, 3]
    )
    def test_genres_listed_are_sorted_and_paginated(
        self,
        current_page: int,
        mock_genre_repository,
    ):
        genre_terror = Genre(name="Terror", is_active=True)
        genre_comedy = Genre(name="Comedy", is_active=False)
        genre_drama = Genre(name="Drama", is_active=True)
        genre_novel = Genre(name="Novel", is_active=False)
        genre_career = Genre(name="Career", is_active=True)

        mock_genre_repository.list.return_value = [
            genre_terror,
            genre_comedy,
            genre_drama,
            genre_novel,
            genre_career,
        ]

        expected_data_per_page = {
            1: [genre_career, genre_comedy],
            2: [genre_drama, genre_novel],
            3: [genre_terror],
        }

        expected_data = [
            GenreOutput(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=genre.categories,
            )
            for genre in expected_data_per_page[current_page]
        ]

        use_case = ListGenre(repository=mock_genre_repository)
        output = use_case.execute(input=ListGenre.Input(
            current_page=current_page,
        ))

        assert output == ListGenre.Output(
            data=expected_data,
            meta=ListOutputMeta(
                current_page=current_page,
                per_page=2,
                total=5,
            )
        )

    def test_when_genre_doesnt_exist_return_empty_data(
        self,
        mock_genre_repository,
    ):
        mock_genre_repository.list.return_value = []

        use_case = ListGenre(repository=mock_genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 0
        assert output == ListGenre.Output(data=[])
