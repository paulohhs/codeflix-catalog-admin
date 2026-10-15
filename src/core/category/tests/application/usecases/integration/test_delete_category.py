from src.core.category.application.usecases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
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

        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(id=category_filme.id)

        assert repository.get_by_id(category_filme.id) is not None

        category_responde = use_case.execute(request=request)
        assert category_responde is None

        assert repository.get_by_id(category_filme.id) is None