from rest_framework.test import APIClient
import pytest

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_movie() -> Category:
    return Category(
        name="Movie",
        description="Movie description",
    )


@pytest.fixture
def category_documentary() -> Category:
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestCategoryAPI:
    def test_list_categories(
        self,
        api_client: APIClient,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = "/api/categories/"
        response = api_client.get(url)

        expected_data = [
            {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            }, 
            {
                "id": str(category_documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active,
            },
        ]

        assert response.status_code == 200
        assert response.data == expected_data
