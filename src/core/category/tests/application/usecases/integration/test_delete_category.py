from src.core.category.application.usecases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)


class TestDeleteCategory:
    def test_delete_category_from_repository(
        self,
        mock_im_category_repository_with_data,
    ):
        (
            movie_category,
            documentary_category,
            repository,
        ) = mock_im_category_repository_with_data

        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(id=movie_category.id)

        assert repository.get_by_id(movie_category.id) is not None

        category_responde = use_case.execute(request=request)
        assert category_responde is None

        assert repository.get_by_id(movie_category.id) is None