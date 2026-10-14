from src.core.category.domain.category_repository import CategoryRepository
from django_project.category_app.models import CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, category_model: CategoryModel):
        self.model = CategoryModel

    def save(self, category: Category) -> None:
        self.model.objects.create(
            id=category.id,
            name=category.name
            description=category.description,
            is_active=category.is_active
        )

    def get_by_id(self, id: UUID) -> Category | None:
        category = self.model.get(id=id)

        return Category(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )

    def list(self) -> list[Category]:
        raise NotImplementedError

    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    def update(self, category: Category) -> None:
        raise NotImplementedError

    
