from src.core.category.application.usecases.list_category import ListOutputMeta
from src.core.category.application.usecases.list_category import (
    CategoryOutput,
    ListCategory, 
    ListCategoryRequest, 
    ListCategoryResponse
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestListCategory:
    def test_return_empty_list(self):
        repository = InMemoryCategoryRepository(categories=[])

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()
        response = use_case.execute(request=request)

        assert isinstance(response, ListCategoryResponse)
        assert response == ListCategoryResponse(data=[], meta=ListOutputMeta(current_page=1, per_page=2, total=0))

    def test_return_existing_categories(self):
        category_filme = Category(
            name="Filme", 
            description="This is a test category",
        )
        category_serie = Category(
            name="Série", 
            description="This is a test category",
        )
        repository = InMemoryCategoryRepository(categories=[category_filme, category_serie])

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
            ],
            meta=ListOutputMeta(current_page=1, per_page=2, total=2)
        )
