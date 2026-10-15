from src.core.category.application.usecases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:
    def test_can_update_category_name_and_description(self):
        category = Category(
            name="Filme", 
            description="This is a test category",
        )
        repository = InMemoryCategoryRepository()
        repository.save(category=category)

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Série",
            description="New description",
        )

        use_case.execute(request=request)

        updated_category = repository.get_by_id(category.id)
        assert updated_category.name == "Série"
        assert updated_category.description == "New description"