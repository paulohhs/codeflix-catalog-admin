from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.usecases.exceptions import CategoryNotFound


@dataclass
class GetCategoryResponse:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class GetCategoryRequest:
    id: UUID


class GetCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: GetCategoryRequest) -> GetCategoryResponse:
        category = self.repository.get_by_id(id=request.id)

        if not category:
            raise CategoryNotFound("Category not found")

        return GetCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
