from src.core.category.application.usecases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)


class TestUpdateCategory:
    def test_update_category_name(self, mock_category_repository_with_data):
        (
            movie_category,
            _,
            repository,
        ) = mock_category_repository_with_data
        repository.get_by_id.return_value = movie_category

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=movie_category.id,
            name="Série"
        )

        use_case.execute(request=request)

        assert movie_category.name == "Série"
        assert movie_category.description == movie_category.description
        repository.update.assert_called_once_with(movie_category)

    def test_update_category_description(self, mock_category_repository_with_data):
        (
            movie_category,
            _,
            repository,
        ) = mock_category_repository_with_data
        repository.get_by_id.return_value = movie_category

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=movie_category.id,
            description="Categoria para filmes"
        )

        use_case.execute(request=request)

        assert movie_category.name == movie_category.name
        assert movie_category.description == "Categoria para filmes"
        repository.update.assert_called_once_with(movie_category)

    def test_can_activate_category(self, mock_category_repository_with_data):
        (
            movie_category,
            _,
            repository,
        ) = mock_category_repository_with_data
        movie_category.is_active = False
        repository.get_by_id.return_value = movie_category

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=movie_category.id,
            is_active=True
        )

        use_case.execute(request=request)

        assert movie_category.is_active is True
        repository.update.assert_called_once_with(movie_category)

    def test_can_deactivate_category(self, mock_category_repository_with_data):
        (
            movie_category,
            _,
            repository,
        ) = mock_category_repository_with_data
        repository.get_by_id.return_value = movie_category

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=movie_category.id,
            is_active=False
        )

        use_case.execute(request=request)

        assert movie_category.is_active is False
        repository.update.assert_called_once_with(movie_category)
