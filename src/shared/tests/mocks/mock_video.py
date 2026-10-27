from decimal import Decimal
from unittest.mock import create_autospec

import pytest

from src.core.video.domain.value_objects import Rating
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.core.video.domain.repository import VideoRepository
from src.core.video.domain.video import Video


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
