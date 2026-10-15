import uuid

import pytest

from src.core.category.application.usecases.exceptions import CategoryNotFound
from src.core.category.application.usecases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestGetCategory:
    def test_get_category_by_id(self):
        category_filme = Category(
            name="Filme", 
            description="This is a test category",
        )
        category_serie = Category(
            name="Serie", 
            description="This is a test category",
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=category_filme.id)
        category_response = use_case.execute(request=request)

        assert category_response == GetCategoryResponse(
            id=category_filme.id,
            name="Filme",
            description="This is a test category",
            is_active=True,
        )

    def test_when_category_does_not_exist_then_raise_exception(self):
        category_filme = Category(
            name="Filme", 
            description="This is a test category",
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme]
        )

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=uuid.uuid4())

        with pytest.raises(CategoryNotFound):
            use_case.execute(request=request)
