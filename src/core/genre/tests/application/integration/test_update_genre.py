from src.core.genre.application.use_cases.update_genre import UpdateGenre


class TestUpdateGenre:
    def test_can_update_genre_attributes(
        self,
        mock_im_category_repository_with_data,
        mock_im_genre_repository_with_data,
    ):
        (
            movie_category,
            documentary_category,
            category_repository
        ) = mock_im_category_repository_with_data

        genre, _, genre_repository = mock_im_genre_repository_with_data

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        input = UpdateGenre.Input(
            id=genre.id,
            name="Terror",
            is_active=False,
            categories={movie_category.id, documentary_category.id}
        )
        use_case.execute(input=input)

        updated_genre = genre_repository.get_by_id(id=genre.id)
        assert updated_genre.id == genre.id
        assert updated_genre.name == input.name
        assert updated_genre.is_active == input.is_active
        assert updated_genre.categories == input.categories
