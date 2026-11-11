import uuid
from unittest.mock import create_autospec

import pytest

from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.core._shared.infrastructure.storage.abstract_storage_service import AbstractStorageService
from src.core._shared.events.abstract_message_bus import AbstractMessageBus


@pytest.mark.django_db
class TestUploadVideo:
    def test_upload_video_media_to_video(
        self,
        mock_video_without_media,
        mock_im_video_repository,
    ):
        video = mock_video_without_media
        mock_im_video_repository.videos = [video]
        mock_storage = create_autospec(AbstractStorageService)
        mock_message_bus = create_autospec(AbstractMessageBus)

        use_case = UploadVideo(
            video_repository=mock_im_video_repository,
            storage_service=mock_storage,
            message_bus=mock_message_bus,
        )
        input = UploadVideo.Input(
            video_id=video.id,
            file_name="video.mp4",
            content=b"video content",
            content_type="video/mp4",
        )
        use_case.execute(input=input)

        mock_storage.store.assert_called_once_with(
            file_path=f"videos/{video.id}/video.mp4",
            content=b"video content",
            content_type="video/mp4",
        )
        video_from_repo = mock_im_video_repository.get_by_id(video.id)
        assert video_from_repo.video == AudioVideoMedia(
            name="video.mp4",
            raw_location=f"videos/{video.id}/video.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO
        )
        mock_message_bus.handle.assert_called_once_with([
            AudioVideoMediaUpdatedIntegrationEvent(
                resource_id=f"{video.id}.{MediaType.VIDEO}",
                file_path=f"videos/{video.id}/video.mp4",
            )
        ])

    def test_when_video_does_not_exist_then_raise_error(
        self,
        mock_im_video_repository,
    ):
        inexist_video_id = uuid.uuid4()
        mock_storage = create_autospec(AbstractStorageService)
        mock_message_bus = create_autospec(AbstractMessageBus)

        use_case = UploadVideo(
            video_repository=mock_im_video_repository,
            storage_service=mock_storage,
            message_bus=mock_message_bus,
        )
        input = UploadVideo.Input(
            video_id=inexist_video_id,
            file_name="video.mp4",
            content=b"video content",
            content_type="video/mp4",
        )

        with pytest.raises(VideoNotFound, match=str(inexist_video_id)):
            use_case.execute(input=input)
