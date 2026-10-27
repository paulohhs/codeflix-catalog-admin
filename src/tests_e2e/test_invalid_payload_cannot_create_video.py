import uuid

import pytest

from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestCannotCreateVideo:
    def test_invalid_payload_cannot_create_video(
        self,
        mock_create_video_valid_payload_without_media,
    ):
        url = '/api/videos/'
        api_client = APIClient()

        # Invalid title
        mock_create_video_valid_payload_without_media["title"] = ""
        create_response = api_client.post(
            url,
            data=mock_create_video_valid_payload_without_media,
        )
        assert create_response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in create_response.text
        assert "This field may not be blank" in create_response.text

        mock_create_video_valid_payload_without_media["title"] = "title"

        # Category entity does not exist
        mock_create_video_valid_payload_without_media["categories"] = [str(uuid.uuid4())]
        create_response = api_client.post(
            url,
            data=mock_create_video_valid_payload_without_media,
        )
        assert create_response.status_code == status.HTTP_400_BAD_REQUEST
        assert create_response.data["error"] == "Categories with provided IDs not found"

        # Category and genre entity does not exist
        mock_create_video_valid_payload_without_media["genres"] = [str(uuid.uuid4())]
        create_response = api_client.post(
            url,
            data=mock_create_video_valid_payload_without_media,
        )
        assert create_response.status_code == status.HTTP_400_BAD_REQUEST
        assert create_response.data["error"] == (
            "Categories with provided IDs not found, Genres with provided IDs not found"
        )
