from unittest.mock import create_autospec

import pytest

from core.video.infra.in_memory_video_repository import InMemoryVideoRepository
from src.core.video.domain.repository import VideoRepository


@pytest.fixture
def mock_video_repository() -> VideoRepository:
    return create_autospec(VideoRepository)


@pytest.fixture
def mock_im_video_repository() -> InMemoryVideoRepository:
    return InMemoryVideoRepository()
