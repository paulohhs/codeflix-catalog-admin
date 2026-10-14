from django.test import TestCase
from rest_framework.test import APITestCase

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        category_filme = Category(
            name="Movie",
            description="Movie description",
        )
        category_serie = Category(
            name="Documentary",
            description="Documentary description",
        )

        repository = DjangoORMCategoryRepository()
        repository.save(category_filme)
        repository.save(category_serie)

        url = "/api/categories/"
        response = self.client.get(url)

        expected_data = [
            {
                "id": str(category_filme.id),
                "name": category_filme.name,
                "description": category_filme.description,
                "is_active": category_filme.is_active,
            }, 
            {
                "id": str(category_serie.id),
                "name": category_serie.name,
                "description": category_serie.description,
                "is_active": category_serie.is_active,
            },
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
