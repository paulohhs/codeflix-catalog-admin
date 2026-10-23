from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core._shared.application.list_response import ListOutput, ListOutputMeta, ListInput


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    @dataclass
    class Input(ListInput):
        pass

    @dataclass
    class Output(ListOutput[CategoryOutput]):
        pass

    def execute(self, input: Input) -> Output:
        categories = self.repository.list()

        sorted_categories = sorted(
            [
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in categories
            ],
            key=lambda category: getattr(category, input.order_by)
        )

        categories_page = self.Output.paginate(
            objects=sorted_categories,
            per_page=input.per_page,
            current_page=input.current_page,
        )

        return self.Output(
            data=categories_page,
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=input.per_page,
                total=len(sorted_categories)
            )
        )
