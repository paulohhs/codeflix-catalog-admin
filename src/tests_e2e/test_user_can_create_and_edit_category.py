import pytest

from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self):
        api_client = APIClient()

        # Verifica que lista esta vazia
        list_response = api_client.get('/api/categories/')
        assert list_response.data == {"data": [], "meta": {'current_page': 1, 'per_page': 2, 'total': 0}}

        # Criar uma categoria
        create_response = api_client.post(
            '/api/categories/',
            data={
                "name": "Movie",
                "description": "Movie description",
            }
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_category_id = create_response.data["id"]

        # Verifica que categoria criada aparece na listagem
        list_response = api_client.get('/api/categories/')
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                }
            ],
            "meta": {'current_page': 1, 'per_page': 2, 'total': 1}
        }

        # Edita categoria criada
        update_response = api_client.put(
            f'/api/categories/{created_category_id}/',
            data={
                "name": "Movie Edited",
                "description": "Movie description edited",
                "is_active": False,
            }
        )
        assert update_response.status_code == status.HTTP_204_NO_CONTENT

        # Verifica que categoria editada aparece na listagem
        list_response = api_client.get('/api/categories/')
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie Edited",
                    "description": "Movie description edited",
                    "is_active": False,
                }
            ],
            "meta": {'current_page': 1, 'per_page': 2, 'total': 1}
        }
