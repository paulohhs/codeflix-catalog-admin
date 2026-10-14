from unittest.mock import create_autospec

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.usecases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(
            name="Filme", 
            description="This is a test category",
        )
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Série"
        )

        use_case.execute(request=request)

        assert category.name == "Série"
        assert category.description == "This is a test category"
        repository.update.assert_called_once_with(category)

    def test_update_category_description(self):
        category = Category(
            name="Filme", 
            description="This is a test category",
        )
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            description="Categoria para filmes"
        )

        use_case.execute(request=request)

        assert category.name == "Filme"
        assert category.description == "Categoria para filmes"
        repository.update.assert_called_once_with(category)

    def test_can_activate_category(self):
        category = Category(
            name="Filme", 
            description="This is a test category",
            is_active=False,
        )
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=True
        )

        use_case.execute(request=request)

        assert category.is_active is True
        repository.update.assert_called_once_with(category)

    def test_can_deactivate_category(self):
        category = Category(
            name="Filme", 
            description="This is a test category",
            is_active=True,
        )
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=False
        )

        use_case.execute(request=request)

        assert category.is_active is False
        repository.update.assert_called_once_with(category)
