import pytest

from src.core.category.application.usecases.list_category import ListOutputMeta
from src.core.category.application.usecases.list_category import (
    CategoryOutput,
    ListCategory,
)


class TestListCategory:
    def test_when_no_categories_in_repository_then_return_empty_list(
        self,
        mock_category_repository,
    ):
        mock_category_repository.list.return_value = []

        use_case = ListCategory(repository=mock_category_repository)
        response = use_case.execute(input=ListCategory.Input())

        assert isinstance(response, ListCategory.Output)
        assert response == ListCategory.Output(
            data=[],
            meta=ListOutputMeta(current_page=1, per_page=2, total=0)
        )

    def test_when_categories_in_repository_then_return_list(
        self,
        mock_category_repository_with_data,
    ):
        (
            movie_category,
            documentary_category,
            repository,
        ) = mock_category_repository_with_data

        use_case = ListCategory(repository=repository)
        response = use_case.execute(input=ListCategory.Input())

        assert isinstance(response, ListCategory.Output)
        assert response == ListCategory.Output(
            data=[
                CategoryOutput(
                    id=documentary_category.id,
                    name=documentary_category.name,
                    description=documentary_category.description,
                    is_active=documentary_category.is_active,
                ),
                CategoryOutput(
                    id=movie_category.id,
                    name=movie_category.name,
                    description=movie_category.description,
                    is_active=movie_category.is_active,
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
        mock_category,
        mock_category_repository,
        order_by: str,
        current_page: int,
    ):
        category_sci_fi = mock_category(
            name="Sci-fi",
            description="A",
        )
        category_novel = mock_category(
            name="Novel",
            description="D",
        )
        category_movie = mock_category(
            name="Movie",
            description="B",
        )
        category_documentary = mock_category(
            name="Documentary",
            description="E",
        )
        category_cartoon = mock_category(
            name="Cartoon",
            description="C",
        )

        mock_category_repository.list.return_value = [
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

        use_case = ListCategory(repository=mock_category_repository)
        input = ListCategory.Input(
            order_by=order_by,
            current_page=current_page
        )
        response = use_case.execute(input=input)

        assert isinstance(response, ListCategory.Output)
        assert response == ListCategory.Output(
            data=expected_data,
            meta=ListOutputMeta(
                current_page=current_page,
                per_page=2,
                total=5,
            )
        )
