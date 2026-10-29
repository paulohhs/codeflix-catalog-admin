import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestCanCreateVideoAndUploadMedia:
    def test_user_can_create_video_and_upload_video_midia(
        self,
        mock_create_video_valid_payload_without_media,
    ):
        url = '/api/videos/'
        api_client = APIClient()

        # Confirma que não existe vídeos na listagem
        list_response = api_client.get(url)
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data["data"] == []

        # Cria um novo vídeo sem media
        create_response = api_client.post(
            url,
            data=mock_create_video_valid_payload_without_media,
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        assert create_response.data['id']

        created_video_id = create_response.data['id']

        expected_data = {
            "data": [
                {
                    "id": created_video_id,
                    "title": mock_create_video_valid_payload_without_media["title"],
                    "description": mock_create_video_valid_payload_without_media["description"],
                    "launch_year": mock_create_video_valid_payload_without_media["launch_year"],
                    "duration": '1.00',
                    "rating": mock_create_video_valid_payload_without_media["rating"],
                    "opened": mock_create_video_valid_payload_without_media["opened"],
                    "published": False,
                    "categories": mock_create_video_valid_payload_without_media["categories"],
                    "genres": mock_create_video_valid_payload_without_media["genres"],
                    "cast_members": mock_create_video_valid_payload_without_media["cast_members"],
                    "banner": None,
                    "thumbnail": None,
                    "thumbnail_half": None,
                    "trailer": None,
                    "video": None,
                }
            ],
            "meta": {
                "current_page": 1,
                "per_page": 2,
                "total": 1,
            }
        }

        # Confirma que o vídeo criado aparece na listagem
        list_response = api_client.get(url)
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == expected_data

        # Confirmação explícita que o vídeo criado não tem video_media
        assert list_response.data["data"][0]["video"] is None

        # Faz upload de video_midia do video
        video_file_mock = SimpleUploadedFile(
            name="video.mp4",
            content=b"images/123123/video.mp4",
            content_type="video/mp4"
        )
        response = APIClient().patch(
            f"/api/videos/{created_video_id}/",
            data={"video_file": video_file_mock},
            format="multipart",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Confirma que o vídeo atualizado aparece na listagem
        # e o vídeo_midia agora existe
        expected_data["data"][0]["video"] = {
            "name": video_file_mock.name,
            "raw_location": f"videos/{created_video_id}/video.mp4",
            "encoded_location": "",
            "status": "PENDING",
        }
        list_response = api_client.get(url)
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == expected_data
