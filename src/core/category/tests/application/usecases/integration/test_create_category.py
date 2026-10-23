from uuid import UUID

from src.core.category.application.usecases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse,
)


class TestCreateCategory:
    def test_create_category_with_valid_data(
        self,
        mock_im_category_repository,
    ):
        use_case = CreateCategory(repository=mock_im_category_repository)
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
        assert len(mock_im_category_repository.categories) == 1

        persisted_category = mock_im_category_repository.categories[0]
        assert persisted_category.id == category_id
        assert persisted_category.name == "Test Category"
        assert persisted_category.description == "This is a test category"
        assert persisted_category.is_active == True
