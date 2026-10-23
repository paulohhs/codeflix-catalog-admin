import uuid
import pytest

from src.core.category.application.usecases.exceptions import (
    CategoryNotFound,
)
from src.core.category.application.usecases.get_category import (
    GetCategory, 
    GetCategoryRequest, 
    GetCategoryResponse
)


class TestGetCategory:
    def test_get_category_by_id(self, mock_category_repository_with_data):
        (
            movie_category,
            _,
            repository,
        ) = mock_category_repository_with_data
        repository.get_by_id.return_value = movie_category

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=movie_category.id)
        category_response = use_case.execute(request=request)

        assert isinstance(category_response, GetCategoryResponse)
        assert category_response == GetCategoryResponse(
            id=movie_category.id,
            name=movie_category.name,
            description=movie_category.description,
            is_active=movie_category.is_active,
        )

    def test_get_category_not_found_then_raise_exception(
        self,
        mock_category_repository,
    ):
        mock_category_repository.get_by_id.return_value = None

        use_case = GetCategory(repository=mock_category_repository)
        request = GetCategoryRequest(id=uuid.uuid4())

        with pytest.raises(CategoryNotFound, match="Category not found"):
            use_case.execute(request=request)
