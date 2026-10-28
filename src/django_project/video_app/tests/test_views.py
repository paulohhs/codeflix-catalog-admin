from decimal import Decimal
from uuid import UUID

import pytest

from rest_framework.test import APIClient
from rest_framework import status

from src.core.video.domain.value_objects import ImageMedia, AudioVideoMedia, MediaStatus
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


@pytest.mark.django_db
class TestListAPI:
    def _create_image_data_expected(
        self, image: ImageMedia
    ) -> dict | None:
        if not image:
            return None

        return {
            "name": image.name,
            "location": image.location,
        }

    def _create_audio_video_data_expected(
        self, audio_video: AudioVideoMedia
    ) -> dict | None:
        if not audio_video:
            return None

        return {
            "name": audio_video.name,
            "raw_location": audio_video.raw_location,
            "encoded_location": audio_video.encoded_location,
            "status": audio_video.status.value,
        }

    def test_when_videos_does_not_exist_then_return_empty_list(self):
        expected_response = {
            "data": [],
            "meta": {
                "current_page": 1,
                "per_page": 2,
                "total": 0,
            }
        }
        url = "/api/videos/"

        response = APIClient().get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_response


    @pytest.mark.parametrize(
        "current_page",
        [1, 2, 3]
    )
    def test_list_video(
        self,
        mock_video,
        video_repository,
        current_page,
    ):
        banner = ImageMedia(name="banner.png", location="images/banner.png")
        video_media = AudioVideoMedia(
            name="video.mp4",
            raw_location="images/123123/video.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
        )
        video_1 = mock_video(title="Video Um", banner=banner)
        video_2 = mock_video(title="Video Dois")
        video_3 = mock_video(title="Video Tres", video=video_media)
        video_4 = mock_video(title="Video Quatro")
        video_5 = mock_video(title="Video Cinco")

        video_repository.save(video=video_1)
        video_repository.save(video=video_2)
        video_repository.save(video=video_3)
        video_repository.save(video=video_4)
        video_repository.save(video=video_5)

        expected_data_per_page = {
            1: [video_5, video_2],
            2: [video_4, video_3],
            3: [video_1]
        }

        def _transform_ids_to_strs(_ids: set[UUID]) -> list[str]:
            return [str(_id) for _id in _ids]

        expected_response = {
            "data": [
                {
                    "id": str(video.id),
                    "title": video.title,
                    "description": video.description,
                    "launch_year": video.launch_year,
                    "opened": video.opened,
                    "rating": video.rating.value,
                    "duration": str(video.duration),
                    "published": video.published,
                    "categories": _transform_ids_to_strs(_ids=video.categories),
                    "genres": _transform_ids_to_strs(_ids=video.genres),
                    "cast_members": _transform_ids_to_strs(_ids=video.cast_members),
                    "banner": self._create_image_data_expected(video.banner),
                    "thumbnail": self._create_image_data_expected(video.thumbnail),
                    "thumbnail_half": self._create_image_data_expected(video.thumbnail_half),
                    "trailer": self._create_audio_video_data_expected(video.trailer),
                    "video": self._create_audio_video_data_expected(video.video),
                } for video in expected_data_per_page[current_page]
            ],
            "meta": {
                "current_page": current_page,
                "per_page": 2,
                "total": 5,
            }
        }
        url = f"/api/videos/?order_by=title&current_page={current_page}"

        response = APIClient().get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_response
