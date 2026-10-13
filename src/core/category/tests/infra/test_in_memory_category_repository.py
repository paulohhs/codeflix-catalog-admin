from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestSave:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name="Test Category"
        )

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category


class TestGetById:
    def test_get_by_id(self):
        category = Category(
            name="Test Category"
        )
        repository = InMemoryCategoryRepository(categories=[category])

        founded_category = repository.get_by_id(category.id)
        assert founded_category is not None
        assert isinstance(founded_category, Category)
        assert founded_category.id == category.id
        assert founded_category.name == category.name
        assert founded_category.description == category.description
        assert founded_category.is_active == category.is_active   
