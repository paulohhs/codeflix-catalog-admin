import uuid

import pytest

from src.core.category.application.usecases.exceptions import CategoryNotFound
from src.core.category.application.usecases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)


class TestGetCategory:
    def test_get_category_by_id(
        self,
        mock_im_category_repository_with_data,
    ):
        (
            movie_category,
            documentary_category,
            repository,
        ) = mock_im_category_repository_with_data

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=movie_category.id)
        category_response = use_case.execute(request=request)

        assert category_response == GetCategoryResponse(
            id=movie_category.id,
            name=movie_category.name,
            description=movie_category.description,
            is_active=movie_category.is_active,
        )

    def test_when_category_does_not_exist_then_raise_exception(
        self,
        mock_im_category_repository_with_data,
    ):
        _, _, repository  = mock_im_category_repository_with_data

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=uuid.uuid4())

        with pytest.raises(CategoryNotFound):
            use_case.execute(request=request)
