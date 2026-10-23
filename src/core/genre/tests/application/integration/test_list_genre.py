from src.core.genre.application.use_cases.list_genre import (
    ListGenre,
    GenreOutput,
)
from src.core._shared.application.list_response import ListOutputMeta


class TestListGenre:
    def test_list_generes_with_associated_categories(
        self,
        mock_im_category_repository_with_data,
        mock_im_genre_repository,
        mock_genre_with_categories,
    ):
        movie_category, documentary_category, _ = mock_im_category_repository_with_data

        genre_repository = mock_im_genre_repository
        genre = mock_genre_with_categories(
            name="Drama",
            categories={movie_category.id, documentary_category.id}
        )
        genre_repository.save(genre)

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories,
                )
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=1,
            )
        )

    def test_when_genre_doesnt_exist_return_empty_data(
        self,
        mock_im_genre_repository
    ):
        use_case = ListGenre(repository=mock_im_genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 0
        assert output == ListGenre.Output(data=[])
