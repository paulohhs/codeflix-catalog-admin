from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.usecases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse,
    InvalidCategoryData,
)
from src.core.category.application.usecases.exceptions import (
    InvalidCategoryData,
)


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="Test Category", 
            description="This is a test category",
            is_active=True,
        )

        category_response = use_case.execute(request=request)
        assert isinstance(category_response, CreateCategoryResponse)
        
        category_id = category_response.id
        assert category_id is not None
        assert isinstance(category_id, UUID)
        assert repository.save.called

    def test_create_category_with_invalid_data(self):
        repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(name="")

        with pytest.raises(InvalidCategoryData, match="name cannot be empty"):
            use_case.execute(request=request)
