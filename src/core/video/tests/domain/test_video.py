import uuid
from decimal import Decimal

import pytest

from src.core.video.domain.value_objects import Rating, ImageMedia, AudioVideoMedia, MediaStatus
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
            launched_year=2021,
            duration=Decimal(),
            published=True,
            rating=Rating.L,
            opened=True,
            categories=category_ids,
            genres=genre_ids,
            cast_members=cast_member_ids,
        )

        assert video.id == video_id
        assert video.title == "Video Title"
        assert video.description == "Title Description"
        assert video.launched_year == 2021
        assert video.duration == Decimal()
        assert video.published == True
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
            id=uuid.uuid4(),
            check_sum="123",
            name="Banner test",
            location="",
        )
        thumbnail = ImageMedia(
            id=uuid.uuid4(),
            check_sum="345",
            name="Thumbnail test",
            location="",
        )
        thumbnail_half = ImageMedia(
            id=uuid.uuid4(),
            check_sum="567",
            name="Thumbnail Half test",
            location="",
        )
        trailer = AudioVideoMedia(
            id=uuid.uuid4(),
            check_sum="789",
            name="Trailer test",
            raw_location="raw test location",
            encoded_location="encoded test location",
            status=MediaStatus.COMPLETED,
        )
        media_video = AudioVideoMedia(
            id=uuid.uuid4(),
            check_sum="910",
            name="Media Video test",
            raw_location="raw test location",
            encoded_location="encoded test location",
            status=MediaStatus.COMPLETED,
        )

        video = Video(
            id=video_id,
            title="Video Title",
            description="Title Description",
            launched_year=2021,
            duration=Decimal(),
            published=True,
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
        assert video.launched_year == 2021
        assert video.duration == Decimal()
        assert video.published == True
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
                launched_year=2021,
                duration=Decimal(),
                published=True,
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
                launched_year=2021,
                duration=Decimal(),
                published=True,
                rating=Rating.L,
                opened=True,
                categories=category_ids,
                genres=genre_ids,
                cast_members=cast_member_ids,
            )
