from unittest.mock import create_autospec

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.usecases.list_category import (
    CategoryOutput,
    ListCategory, 
    ListCategoryRequest, 
    ListCategoryResponse
)
from src.core.category.domain.category import Category


class TestListCategory:
    def test_when_no_categories_in_repository_then_return_empty_list(self):
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = []

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()
        response = use_case.execute(request=request)

        assert isinstance(response, ListCategoryResponse)
        assert response == ListCategoryResponse(data=[])

    def test_when_categories_in_repository_then_return_list(self):
        category_filme = Category(
            name="Filme", 
            description="This is a test category",
        )
        category_serie = Category(
            name="Série", 
            description="This is a test category",
        )
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = [category_filme, category_serie]

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()
        response = use_case.execute(request=request)

        assert isinstance(response, ListCategoryResponse)
        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_filme.id,
                    name=category_filme.name,
                    description=category_filme.description,
                    is_active=category_filme.is_active,
                ),
                CategoryOutput(
                    id=category_serie.id,
                    name=category_serie.name,
                    description=category_serie.description,
                    is_active=category_serie.is_active,
                )
            ]
        )
