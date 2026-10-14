from django.test import TestCase
import pytest

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


class TestCategoryAPI:
    @pytest.fixture
    def category_movie(self) -> Category:
        return Category(
            name="Movie",
            description="Movie description",
        )

    @pytest.fixture
    def category_documentary(self) -> Category:
        return Category(
            name="Movie",
            description="Movie description",
        )

    @pytest.fixture
    def category_repository(self) -> DjangoORMCategoryRepository:
        return DjangoORMCategoryRepository()
    
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = "/api/categories/"
        response = self.client.get(url)

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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
