import uuid
from decimal import Decimal

import pytest

from rest_framework.test import APIClient
from rest_framework import status

from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video


@pytest.mark.django_db
class TestCanCreateVideo:
    def test_user_can_create_video_without_media(
        self,
        mock_create_video_valid_payload_without_media,
        video_repository,
    ):
        url = '/api/videos/'
        api_client = APIClient()

        # TODO: trocar por consulta na api de listagem
        assert video_repository.list() == []

        create_response = api_client.post(
            url,
            data=mock_create_video_valid_payload_without_media,
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        assert create_response.data['id']

        # TODO: trocar por consulta na api de listagem
        assert video_repository.list() == [
            Video(
                id=uuid.UUID(create_response.data['id']),
                title=mock_create_video_valid_payload_without_media["title"],
                description=mock_create_video_valid_payload_without_media["description"],
                launch_year=mock_create_video_valid_payload_without_media["launch_year"],
                duration=Decimal(mock_create_video_valid_payload_without_media["duration"]),
                rating=Rating(mock_create_video_valid_payload_without_media["rating"]),
                opened=mock_create_video_valid_payload_without_media["opened"],
                categories={
                    uuid.UUID(obj_id) for obj_id in
                    mock_create_video_valid_payload_without_media["categories"]
                },
                genres={
                    uuid.UUID(obj_id) for obj_id in
                    mock_create_video_valid_payload_without_media["genres"]
                },
                cast_members={
                    uuid.UUID(obj_id) for obj_id in
                    mock_create_video_valid_payload_without_media["cast_members"]
                },
            )
        ]
