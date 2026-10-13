from unittest.mock import create_autospec
import uuid

import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.usecases.exceptions import (
    CategoryNotFound,
)
from src.core.category.application.usecases.get_category import (
    GetCategory, 
    GetCategoryRequest, 
    GetCategoryResponse
)
from src.core.category.domain.category import Category


class TestGetCategory:
    def test_get_category_by_id(self):
        category = Category(
            name="Filme", 
            description="This is a test category",
        )
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=category.id)
        category_response = use_case.execute(request=request)

        assert isinstance(category_response, GetCategoryResponse)
        assert category_response == GetCategoryResponse(
            id=category.id,
            name="Filme",
            description="This is a test category",
            is_active=True,
        )

    def test_get_category_not_found_then_raise_exception(self):
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = None

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=uuid.uuid4())

        with pytest.raises(CategoryNotFound, match="Category not found"):
            use_case.execute(request=request)
