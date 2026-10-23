from src.core.category.application.usecases.list_category import ListOutputMeta
from src.core.category.application.usecases.list_category import (
    CategoryOutput,
    ListCategory,
)


class TestListCategory:
    def test_return_empty_list(
        self,
        mock_im_category_repository,
    ):
        use_case = ListCategory(repository=mock_im_category_repository)
        response = use_case.execute(input=ListCategory.Input())

        assert isinstance(response, ListCategory.Output)
        assert response == ListCategory.Output(
            data=[],
            meta=ListOutputMeta(current_page=1, per_page=2, total=0)
        )

    def test_return_existing_categories(
        self,
        mock_im_category_repository_with_data,
    ):
        (
            movie_category,
            documentary_category,
            repository,
        ) = mock_im_category_repository_with_data

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
