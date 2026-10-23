import uuid
import pytest

from src.core.category.application.usecases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.application.usecases.exceptions import CategoryNotFound


class TestDeleteCategory:
    def test_delete_category_from_repository(
        self,
        mock_category_repository_with_data,
    ):
        (
            movie_category,
            _,
            repository,
        ) = mock_category_repository_with_data
        repository.get_by_id.return_value = movie_category

        use_case = DeleteCategory(repository=repository)
        use_case.execute(DeleteCategoryRequest(id=movie_category.id))

        repository.delete.assert_called_once_with(id=movie_category.id)

    def test_when_category_not_found_then_raise_exception(
        self,
        mock_category_repository,
    ):
        mock_category_repository.get_by_id.return_value = None

        use_case = DeleteCategory(repository=mock_category_repository)
        with pytest.raises(CategoryNotFound, match="Category not found"):
            use_case.execute(request=DeleteCategoryRequest(id=uuid.uuid4()))

        mock_category_repository.delete.assert_not_called()
