import pytest

from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestUserCanCreateEditAndDeleteCastMember:
    def test_user_can_create_edit_and_delete_cast_member(self):
        api_client = APIClient()

        # Verifica que lista esta vazia
        list_response = api_client.get('/api/cast_members/')
        assert list_response.data == {"data": []}

        # Criar um cast member
        create_response = api_client.post(
            '/api/cast_members/',
            data={
                "name": "Actor Member",
                "type": "ACTOR",
            }
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_cast_member_id = create_response.data["id"]

        # Verifica que cast member criado aparece na listagem
        # e está ativa
        list_response = api_client.get('/api/cast_members/')
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == {
            "data": [
                {
                    "id": created_cast_member_id,
                    "name": "Actor Member",
                    "type": "ACTOR",
                }
            ]
        }

        # Atualiza cast member
        update_response = api_client.put(
            f'/api/cast_members/{created_cast_member_id}/',
            data={
                "name": "Member updated",
                "type": "DIRECTOR",
            }
        )
        assert update_response.status_code == status.HTTP_204_NO_CONTENT

        # Verifica que cast member foi atualizado
        list_response = api_client.get('/api/cast_members/')
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data["data"][0]["id"] == created_cast_member_id
        assert list_response.data["data"][0]["name"] == "Member updated"
        assert list_response.data["data"][0]["type"] == "DIRECTOR"

        # Deleta cast member
        delete_response = api_client.delete(f'/api/cast_members/{created_cast_member_id}/')
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # Verifica que cast member deletado não esta na lista
        list_response = api_client.get('/api/cast_members/')
        assert list_response.data == {"data": []}
