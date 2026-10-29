from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from src.core.video.domain.value_objects import ImageMedia, AudioVideoMedia
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.repository import VideoRepository
from src.core._shared.application.list_response import ListOutput, ListOutputMeta, ListInput


@dataclass
class VideoOutput:
    id: UUID
    title: str
    description: str
    launch_year: int
    duration: Decimal
    rating: Rating
    opened: bool
    published: bool
    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None


class ListVideo:
    def __init__(self, repository: VideoRepository):
        self.repository = repository

    @dataclass
    class Input(ListInput):
        pass

    @dataclass
    class Output(ListOutput[VideoOutput]):
        pass

    def execute(self, input: Input) -> Output:
        videos = self.repository.list()

        sorted_videos = sorted(
            [
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
                    banner=video.banner,
                    thumbnail=video.thumbnail,
                    thumbnail_half=video.thumbnail_half,
                    trailer=video.trailer,
                    video=video.video,
                ) for video in videos
            ],
            key=lambda video: getattr(video, input.order_by)
        )

        genres_page = self.Output.paginate(
            objects=sorted_videos,
            per_page=input.per_page,
            current_page=input.current_page,
        )

        return self.Output(
            data=genres_page,
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=input.per_page,
                total=len(sorted_videos)
            )
        )