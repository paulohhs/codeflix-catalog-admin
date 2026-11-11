from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from src.core.video.domain.value_objects import MediaStatus, MediaType
from src.core.video.domain.value_objects import (
    Rating,
    ImageMedia,
    AudioVideoMedia,
)
from src.core._shared.domain.entity import Entity
from src.core.video.domain.events.events import AudioVideoMediaUpdated


@dataclass
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    rating: Rating
    opened: bool
    published: bool = field(default=False, init=False)

    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]

    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None

    def __post_init__(self):
        self.validate()


    def validate(self):
        if len(self.title) > 255:
            self.notification.add_error("title cannot be longer than 255")

        if not self.title:
            self.notification.add_error("title cannot be empty")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update(
        self,
        title: str,
        description: str,
        launch_year: int,
        duration: Decimal,
        published: bool,
        rating: Rating,
        opened: bool,
        categories: set[UUID],
        genres: set[UUID],
        cast_members: set[UUID],
    ):
        self.title = title
        self.description = description
        self.launch_year = launch_year
        self.duration = duration
        self.published = published
        self.rating = rating
        self.opened = opened
        self.categories = categories
        self.genres = genres
        self.cast_members = cast_members

        self.validate()

    def publish(self) -> None:
        if not self.video:
            self.notification.add_error("Video media is required to publish the video")
        elif self.video.status != MediaStatus.COMPLETED:
            self.notification.add_error("Video must be fully processed to be published")

        self.published = True
        self.validate()

    def add_category(self, category_id: UUID) -> None:
        self.categories.add(category_id)
        self.validate()

    def add_genre(self, genre_id: UUID) -> None:
        self.genres.add(genre_id)
        self.validate()

    def add_cast_member(self, cast_member_id: UUID) -> None:
        self.cast_members.add(cast_member_id)
        self.validate()

    def update_banner(self, banner: ImageMedia) -> None:
        self.banner = banner
        self.validate()

    def update_thumbnail(self, thumbnail: ImageMedia) -> None:
        self.thumbnail = thumbnail
        self.validate()

    def update_thumbnail_half(self, thumbnail_half: ImageMedia) -> None:
        self.thumbnail_half = thumbnail_half
        self.validate()

    def update_trailer(self, trailer: AudioVideoMedia) -> None:
        self.trailer = trailer
        self.validate()

    def update_video_media(self, video: AudioVideoMedia) -> None:
        self.video = video
        self.validate()

        self.dispatch(AudioVideoMediaUpdated(
            aggregate_id=self.id,
            file_path=video.raw_location,
            media_type=MediaType.VIDEO,
        ))

    def process(self, status, encoded_location):
        if status == MediaStatus.COMPLETED:
            self.video = self.video.complete(encoded_location)
            self.publish()
        else:
            self.video = self.video.fail()

        self.validate()

    def validate_audio_video_media_to_process(
        self,
        media_type: MediaType,
    ) -> None:
        video_type = MediaType.VIDEO
        trailer_type = MediaType.TRAILER

        error = None

        if media_type not in [video_type, trailer_type]:
            error = "The media type must be VIDEO or TRAILER"

        elif media_type == MediaType.VIDEO:
            if not self.video:
                error = "Video must have media to be processed"

        elif media_type == MediaType.TRAILER:
            if not self.trailer:
                error = "Video must have media to be processed"

        if error:
            self.notification.add_error(error)
            self.validate()
