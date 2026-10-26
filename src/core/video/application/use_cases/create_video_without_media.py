from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core.video.application.use_cases.exceptions import (
    InvalidVideo,
    RelatedEntitiesNotFound,
)
from src.core._shared.domain.notification import Notification
from src.core.video.domain.repository import VideoRepository
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository



class CreateVideoWithoutMedia:
    @dataclass
    class Input:
        title: str
        description: str
        launched_year: int
        duration: Decimal
        rating: str
        opened: bool
        categories: set[UUID]
        genres: set[UUID]
        cast_members: set[UUID]

    @dataclass
    class Output:
        id: UUID

    def __init__(
        self,
        video_repository: VideoRepository,
        category_repository: CategoryRepository,
        genre_repository: GenreRepository,
        cast_member_repository: CastMemberRepository,
    ) -> None:
        self.video_repository = video_repository
        self.category_repository = category_repository
        self.genre_repository = genre_repository
        self.cast_member_repository = cast_member_repository

    def execute(self, input: Input) -> Output:
        notification = Notification()

        self.validate_categories(input=input, notification=notification)
        self.validate_genres(input=input, notification=notification)
        self.validate_cast_members(input=input, notification=notification)

        if notification.has_errors:
            raise RelatedEntitiesNotFound(notification.messages)

        try:
            video = Video(
                title=input.title,
                description=input.description,
                launched_year=input.launched_year,
                duration=input.duration,
                published=False,
                rating=Rating(input.rating),
                opened=input.opened,
                categories=input.categories,
                genres=input.genres,
                cast_members=input.cast_members,
            )
        except ValueError as err:
            raise InvalidVideo(err)

        self.video_repository.save(video)

        return self.Output(id=video.id)

    def validate_categories(
        self,
        input: Input,
        notification: Notification,
    ) -> None:
        categories = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(categories):
            notification.add_error("Categories with provided IDs not found")

    def validate_genres(
        self,
        input: Input,
        notification: Notification,
    ) -> None:
        genres = {genre.id for genre in self.genre_repository.list()}
        if not input.genres.issubset(genres):
            notification.add_error("Genres with provided IDs not found")

    def validate_cast_members(
        self,
        input: Input,
        notification: Notification,
    ) -> None:
        cast_members = {cast_member.id for cast_member in self.cast_member_repository.list()}
        if not input.cast_members.issubset(cast_members):
            notification.add_error("Cast Members with provided IDs not found")
