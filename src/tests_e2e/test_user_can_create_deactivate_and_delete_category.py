import pytest

from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestCreateDeactivateAndDeleteCategory:
    def test_user_can_create_deactivate_and_delete_category(self):
        api_client = APIClient()

        # Verifica que lista esta vazia
        list_response = api_client.get('/api/categories/')
        assert list_response.data == {"data": []}

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
        # e está ativa
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
            ]
        }

        # Desativa categoria criada
        update_response = api_client.patch(
            f'/api/categories/{created_category_id}/',
            data={
                "is_active": False,
            }
        )
        assert update_response.status_code == status.HTTP_204_NO_CONTENT

        # Verifica que categoria foi desativada
        list_response = api_client.get('/api/categories/')
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data["data"][0]["is_active"] is False

        # Deleta categoria
        delete_response = api_client.delete(f'/api/categories/{created_category_id}/')
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # Verifica que categoria deletada não esta na lista
        list_response = api_client.get('/api/categories/')
        assert list_response.data == {"data": []}
