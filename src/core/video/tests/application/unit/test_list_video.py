import uuid

import pytest

from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus
from src.core.video.application.use_cases.list_video import ListVideo, VideoOutput

from decimal import Decimal
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core._shared.application.list_response import ListOutputMeta


class TestListVideo:
    @pytest.mark.parametrize("with_media", [True, False])
    def test_list_video(
        self,
        mock_video_repository,
        with_media,
    ):
        video_media = None

        if with_media:
            video_media = AudioVideoMedia(
                name="video.mp4",
                raw_location=f"videos/123123123/video.mp4",
                encoded_location="",
                status=MediaStatus.COMPLETED,
            )

        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.50"),
            rating=Rating.AGE_12,
            categories={uuid.uuid4()},
            genres={uuid.uuid4()},
            cast_members={uuid.uuid4()},
            opened=True,
            video=video_media,
        )
        mock_video_repository.list.return_value = [video]
        use_case = ListVideo(repository=mock_video_repository)
        output = use_case.execute(input=ListVideo.Input(order_by="title"))

        assert output == ListVideo.Output(
            data=[
                VideoOutput(
                    id=video.id,
                    title=video.title,
                    description=video.description,
                    launch_year=video.launch_year,
                    duration=video.duration,
                    rating=video.rating,
                    opened=video.opened,
                    published=video.published,
                    categories=video.categories,
                    genres=video.genres,
                    cast_members=video.cast_members,
                    video=video.video,
                )
            ],
            meta=ListOutputMeta(current_page=1, per_page=2, total=1)
        )


    def test_when_videos_doesnt_exist_return_empty_data(
        self,
        mock_video_repository,
    ):
        mock_video_repository.list.return_value = []

        use_case = ListVideo(repository=mock_video_repository)
        output = use_case.execute(input=ListVideo.Input())

        assert len(output.data) == 0
        assert output == ListVideo.Output(data=[])

