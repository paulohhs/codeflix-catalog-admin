from src.core.category.application.usecases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)


class TestUpdateCategory:
    def test_can_update_category_name_and_description(
        self,
        mock_im_category_repository_with_data,
    ):
        (
            movie_category,
            _,
            repository,
        ) = mock_im_category_repository_with_data

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=movie_category.id,
            name="Série",
            description="New description",
        )

        use_case.execute(request=request)

        updated_category = repository.get_by_id(movie_category.id)
        assert updated_category.name == "Série"
        assert updated_category.description == "New description"