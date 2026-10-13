from unittest.mock import create_autospec
import uuid

import pytest

from src.core.category.application.category_repository import (
    CategoryRepository,
)
from src.core.category.application.usecases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.application.usecases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(
            name="Test Category",
            description="Test category description"
        )
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category

        use_case = DeleteCategory(repository=repository)
        use_case.execute(DeleteCategoryRequest(id=category.id))

        repository.delete.assert_called_once_with(id=category.id)

    def test_when_category_not_found_then_raise_exception(self):
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = None

        use_case = DeleteCategory(repository=repository)
        with pytest.raises(CategoryNotFound, match="Category not found"):
            use_case.execute(request=DeleteCategoryRequest(id=uuid.uuid4()))

        repository.delete.assert_not_called()
