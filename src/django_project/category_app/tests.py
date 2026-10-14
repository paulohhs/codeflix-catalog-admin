from django.test import TestCase
from rest_framework.test import APITestCase


class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        url = "/api/categories/"
        response = self.client.get(url)

        expected_data = [
            {
                "id": "632469e0-d6f3-42b1-b349-e47ed1e79cc4",
                "name": "Movie",
                "description": "Movie description",
                "is_active": True,
            }, 
            {
                "id": "f0efc68b-28f5-48ae-9544-cd74a0991270",
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True,
            },
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
