from uuid import UUID

from src.core.category.application.usecases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse,
)
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
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
        assert len(repository.categories) == 1

        persisted_category = repository.categories[0]
        assert persisted_category.id == category_id
        assert persisted_category.name == "Test Category"
        assert persisted_category.description == "This is a test category"
        assert persisted_category.is_active == True
