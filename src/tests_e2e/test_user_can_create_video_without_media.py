import pytest

from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestCanCreateVideo:
    def test_user_can_create_video_without_media(
        self,
        mock_create_video_valid_payload_without_media,
    ):
        url = '/api/videos/'
        api_client = APIClient()

        list_response = api_client.get(url)
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data["data"] == []

        create_response = api_client.post(
            url,
            data=mock_create_video_valid_payload_without_media,
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        assert create_response.data['id']

        expected_data = {
            "data": [
                {
                    "id": create_response.data['id'],
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

        list_response = api_client.get(url)
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == expected_data
