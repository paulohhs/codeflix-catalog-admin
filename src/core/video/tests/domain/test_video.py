import uuid
from decimal import Decimal

import pytest

from src.core.video.domain.events.events import AudioVideoMediaUpdated
from src.core.video.domain.value_objects import (
    Rating,
    ImageMedia,
    AudioVideoMedia,
    MediaStatus,
    MediaType,
)
from src.core.video.domain.video import Video


class TestVideo:
    def test_video_is_created_with_provided_required_values(self):
        video_id = uuid.uuid4()
        category_ids = {uuid.uuid4(), uuid.uuid4()}
        genre_ids = {uuid.uuid4(), uuid.uuid4()}
        cast_member_ids = {uuid.uuid4(), uuid.uuid4()}

        video = Video(
            id=video_id,
            title="Video Title",
            description="Title Description",
            launch_year=2021,
            duration=Decimal(),
            rating=Rating.L,
            opened=True,
            categories=category_ids,
            genres=genre_ids,
            cast_members=cast_member_ids,
        )

        assert video.id == video_id
        assert video.title == "Video Title"
        assert video.description == "Title Description"
        assert video.launch_year == 2021
        assert video.duration == Decimal()
        assert video.published == False
        assert video.rating == Rating.L
        assert video.categories == category_ids
        assert video.genres == genre_ids
        assert video.cast_members == cast_member_ids

    def test_video_is_created_with_provided_all_values(self):
        video_id = uuid.uuid4()
        category_ids = {uuid.uuid4(), uuid.uuid4()}
        genre_ids = {uuid.uuid4(), uuid.uuid4()}
        cast_member_ids = {uuid.uuid4(), uuid.uuid4()}
        banner = ImageMedia(
            name="Banner test",
            raw_location="",
        )
        thumbnail = ImageMedia(
            name="Thumbnail test",
            raw_location="",
        )
        thumbnail_half = ImageMedia(
            name="Thumbnail Half test",
            raw_location="",
        )
        trailer = AudioVideoMedia(
            name="Trailer test",
            raw_location="raw test location",
            encoded_location="encoded test location",
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO
        )
        media_video = AudioVideoMedia(
            name="Media Video test",
            raw_location="raw test location",
            encoded_location="encoded test location",
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO
        )

        video = Video(
            id=video_id,
            title="Video Title",
            description="Title Description",
            launch_year=2021,
            duration=Decimal(),
            rating=Rating.L,
            opened=True,
            categories=category_ids,
            genres=genre_ids,
            cast_members=cast_member_ids,
            banner=banner,
            thumbnail=thumbnail,
            thumbnail_half=thumbnail_half,
            trailer=trailer,
            video=media_video,
        )

        assert video.id == video_id
        assert video.title == "Video Title"
        assert video.description == "Title Description"
        assert video.launch_year == 2021
        assert video.duration == Decimal()
        assert video.published == False
        assert video.rating == Rating.L
        assert video.categories == category_ids
        assert video.genres == genre_ids
        assert video.cast_members == cast_member_ids
        assert video.banner == banner
        assert video.thumbnail == thumbnail
        assert video.thumbnail_half == thumbnail_half
        assert video.trailer == trailer
        assert video.video == media_video

    def test_when_title_is_invalid_then_raise_error(self):
        video_id = uuid.uuid4()
        category_ids = {uuid.uuid4(), uuid.uuid4()}
        genre_ids = {uuid.uuid4(), uuid.uuid4()}
        cast_member_ids = {uuid.uuid4(), uuid.uuid4()}

        with pytest.raises(ValueError, match="title cannot be empty"):
            Video(
                id=video_id,
                title="",
                description="Title Description",
                launch_year=2021,
                duration=Decimal(),
                rating=Rating.L,
                opened=True,
                categories=category_ids,
                genres=genre_ids,
                cast_members=cast_member_ids,
            )

        with pytest.raises(ValueError, match="title cannot be longer than 255"):
            Video(
                id=video_id,
                title="a" * 256,
                description="Title Description",
                launch_year=2021,
                duration=Decimal(),
                rating=Rating.L,
                opened=True,
                categories=category_ids,
                genres=genre_ids,
                cast_members=cast_member_ids,
            )


class TestPublish:
    def test_publish_video_without_media(
        self,
        mock_video_without_association: Video
    ) -> None:
        with pytest.raises(ValueError, match="Video media is required to publish the video"):
            mock_video_without_association.publish()

    def test_publish_video_with_pending_media(
        self,
        mock_video_without_association: Video
    ) -> None:
        mock_video_without_association.video = AudioVideoMedia(
            name="video.mp4",
            raw_location="raw_path",
            encoded_location="",
            status=MediaStatus.PROCESSING,
            media_type=MediaType.VIDEO,
        )
        with pytest.raises(ValueError, match="Video must be fully processed to be published"):
            mock_video_without_association.publish()

    def test_publish_video_with_completed_media(
        self,
        mock_video_without_association: Video
    ) -> None:
        mock_video_without_association.video = AudioVideoMedia(
            name="video.mp4",
            raw_location="raw_path",
            encoded_location="encoded_path",
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        mock_video_without_association.publish()
        assert mock_video_without_association.published is True


class TestUpdateVideoMedia:
    def test_update_video_and_append_event(self, mock_video_without_association: Video) -> None:
        media = AudioVideoMedia(
            name="video.mp4",
            raw_location="raw_path",
            encoded_location="encoded_path",
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        mock_video_without_association.update_video_media(media)
        assert mock_video_without_association.video == media
        # assert mock_video_without_association.events == [AudioVideoMediaUpdated(
        #     aggregate_id=mock_video_without_association.id,
        #     file_path=media.raw_location,
        #     media_type=MediaType.VIDEO,
        # )]


class TestProcess:
    def test_process_audio_video_media_completed_and_publish(
        self,
        mock_video_without_association: Video
    ) -> None:
        original_encoded_location = "encoded_path"
        media = AudioVideoMedia(
            name="video.mp4",
            raw_location="raw_path",
            encoded_location=original_encoded_location,
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        mock_video_without_association.video = media

        # completed and publish
        mock_video_without_association.process(
            status=MediaStatus.COMPLETED,
            encoded_location="encoded_location_test",
        )
        assert mock_video_without_association.video.status == MediaStatus.COMPLETED
        assert mock_video_without_association.video.encoded_location == "encoded_location_test"
        assert mock_video_without_association.published is True

    def test_process_audio_video_fail(
        self,
        mock_video_without_association: Video
    ) -> None:
        original_encoded_location = "encoded_path"
        media = AudioVideoMedia(
            name="video.mp4",
            raw_location="raw_path",
            encoded_location=original_encoded_location,
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        mock_video_without_association.video = media

        mock_video_without_association.process(
            status=MediaStatus.PROCESSING,
            encoded_location="encoded_location_test",
        )
        assert mock_video_without_association.video.status == MediaStatus.ERROR
        assert mock_video_without_association.video.encoded_location == original_encoded_location
        assert mock_video_without_association.published is False
