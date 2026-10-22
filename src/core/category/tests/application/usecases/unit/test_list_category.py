from unittest.mock import create_autospec

import pytest

from src.core.category.application.usecases.list_category import ListOutputMeta
from src.core.category.domain.category_repository import CategoryRepository
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
        assert response == ListCategoryResponse(
            data=[],
            meta=ListOutputMeta(current_page=1, per_page=2, total=0)
        )

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
            ],
            meta=ListOutputMeta(current_page=1, per_page=2, total=2)
        )

    @pytest.mark.parametrize(
        "order_by, current_page",
        [
            ("name", 1),
            ("name", 2),
            ("name", 3),
            ("description", 1),
            ("description", 2),
            ("description", 3),
        ]
    )
    def test_sorting_name_and_pagination_then_return_list(
        self,
        order_by: str,
        current_page: int,
    ):
        category_sci_fi = Category(
            name="Sci-fi",
            description="A",
        )
        category_novel = Category(
            name="Novel",
            description="D",
        )
        category_movie = Category(
            name="Movie",
            description="B",
        )
        category_documentary = Category(
            name="Documentary",
            description="E",
        )
        category_cartoon = Category(
            name="Cartoon",
            description="C",
        )

        repository = create_autospec(CategoryRepository)
        repository.list.return_value = [
            category_sci_fi,
            category_novel,
            category_movie,
            category_documentary,
            category_cartoon,
        ]

        if order_by == "name":
            expected_data_per_page = {
                1: [category_cartoon, category_documentary],
                2: [category_movie, category_novel],
                3: [category_sci_fi],
            }
        else:
            expected_data_per_page = {
                1: [category_sci_fi, category_movie],
                2: [category_cartoon, category_novel],
                3: [category_documentary],
            }

        expected_data = [
            CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
            for category in expected_data_per_page[current_page]
        ]

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest(
            order_by=order_by,
            current_page=current_page
        )
        response = use_case.execute(request=request)

        assert isinstance(response, ListCategoryResponse)
        assert response == ListCategoryResponse(
            data=expected_data,
            meta=ListOutputMeta(
                current_page=current_page,
                per_page=2,
                total=5,
            )
        )
