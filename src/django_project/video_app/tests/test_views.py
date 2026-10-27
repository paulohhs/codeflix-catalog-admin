from decimal import Decimal
from uuid import UUID

import pytest

from rest_framework.test import APIClient
from rest_framework import status

from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid_then_return_400(
        self,
        mock_create_video_valid_payload_without_media,
    ):
        url = '/api/videos/'

        mock_create_video_valid_payload_without_media["title"] = ""
        response = APIClient().post(
            url,
            data=mock_create_video_valid_payload_without_media
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_payload_is_valid_then_create_video_and_return_201(
        self,
        mock_create_video_valid_payload_without_media,
        video_repository,
    ):
        url = '/api/videos/'

        response = APIClient().post(
            url,
            data=mock_create_video_valid_payload_without_media
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]

        created_video = video_repository.get_by_id(response.data["id"])
        assert created_video == Video(
            id=UUID(response.data["id"]),
            title=mock_create_video_valid_payload_without_media["title"],
            description=mock_create_video_valid_payload_without_media["description"],
            launch_year=mock_create_video_valid_payload_without_media["launch_year"],
            opened=mock_create_video_valid_payload_without_media["opened"],
            rating=Rating(mock_create_video_valid_payload_without_media["rating"]),
            duration=Decimal(mock_create_video_valid_payload_without_media["duration"]),
            categories={
                UUID(mock_create_video_valid_payload_without_media["categories"][0])
            },
            genres={
                UUID(mock_create_video_valid_payload_without_media["genres"][0])
            },
            cast_members={
                UUID(mock_create_video_valid_payload_without_media["cast_members"][0])
            }
        )
