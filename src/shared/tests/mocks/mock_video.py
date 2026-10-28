from decimal import Decimal
from unittest.mock import create_autospec
from uuid import UUID

import pytest

from src.core.video.domain.value_objects import ImageMedia, AudioVideoMedia
from src.core.video.domain.value_objects import Rating
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.core.video.domain.repository import VideoRepository
from src.core.video.domain.video import Video


@pytest.fixture
def mock_video(
    mock_movie_category,
    category_repository_with_data,
    genre_repository_with_data,
    cast_member_repository_with_data
) -> callable:
    def make_mock(
        title: str = "Mock Test Video",
        description: str = "A test video",
        launch_year: int = 2022,
        duration: Decimal = Decimal("120.50"),
        rating: Rating = Rating.AGE_12,
        opened: bool = True,
        categories: set[UUID] | None = None,
        genres: set[UUID] | None = None,
        cast_members: set[UUID] | None = None,
        banner: ImageMedia | None = None,
        thumbnail: ImageMedia | None = None,
        thumbnail_half: ImageMedia | None = None,
        trailer: AudioVideoMedia | None = None,
        video: AudioVideoMedia | None = None,
    ) -> Video:
        mock_new_genre, _, _ = genre_repository_with_data
        mock_new_cast_member, _, _ = cast_member_repository_with_data

        return Video(
            title=title,
            description=description,
            launch_year=launch_year,
            duration=duration,
            rating=rating,
            categories=categories if categories else {mock_movie_category.id},
            genres=genres if genres else {mock_new_genre.id},
            cast_members=cast_members if cast_members else {mock_new_cast_member.id},
            opened=opened,
            banner=banner,
            thumbnail=thumbnail,
            thumbnail_half=thumbnail_half,
            trailer=trailer,
            video=video,
        )

    yield make_mock


@pytest.fixture
def mock_video_without_media(
    mock_movie_category,
    category_repository_with_data,
    genre_repository_with_data,
    cast_member_repository_with_data
) -> Video:
    genre, _, _ = genre_repository_with_data
    cast_member, _, _ = cast_member_repository_with_data

    return Video(
        title="Sample Video",
        description="A test video",
        launch_year=2022,
        duration=Decimal("120.50"),
        rating=Rating.AGE_12,
        categories={mock_movie_category.id},
        genres={genre.id},
        cast_members={cast_member.id},
        opened=True,
    )


@pytest.fixture
def mock_video_repository() -> VideoRepository:
    return create_autospec(VideoRepository)


@pytest.fixture
def mock_im_video_repository() -> InMemoryVideoRepository:
    return InMemoryVideoRepository()


@pytest.fixture
def video_repository() -> DjangoORMVideoRepository:
    return DjangoORMVideoRepository()


@pytest.fixture
def mock_create_video_valid_payload_without_media(
    mock_movie_category,
    category_repository_with_data,
    genre_repository_with_data,
    cast_member_repository_with_data,
) -> dict:
    genre, _, _ = genre_repository_with_data
    cast_member, _, _ = cast_member_repository_with_data

    return {
        "title": "title",
        "description": "description",
        "launch_year": 2019,
        "opened": True,
        "rating": "L",
        "duration": 1.00,
        "categories": [str(mock_movie_category.id)],
        "genres": [str(genre.id)],
        "cast_members": [str(cast_member.id)]
    }
