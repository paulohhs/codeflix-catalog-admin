from uuid import UUID

from django.db import transaction

from src.core.video.domain.value_objects import MediaStatus
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.value_objects import AudioVideoMedia
from src.core.video.domain.video import Video
from src.core.video.domain.repository import VideoRepository
from src.core.video.domain.value_objects import ImageMedia
from src.django_project.video_app.models import (
    Video as VideoORM,
    AudioVideoMedia as AudioVideoMediaORM,
    ImageMedia as ImageMediaORM,
)


class DjangoORMVideoRepository(VideoRepository):
    def _save_medias(self, video_model: VideoORM) -> None:
        for media in [
            video_model.banner,
            video_model.thumbnail,
            video_model.thumbnail_half,
            video_model.trailer,
            video_model.video,
        ]:
            if media:
                media.save()

    def _delete_medias(self, video_model: VideoORM) -> None:
        for media in [
            video_model.banner,
            video_model.thumbnail,
            video_model.thumbnail_half,
            video_model.trailer,
            video_model.video,
        ]:
            if media:
                media.delete()

    def save(self, video: Video) -> None:
        with transaction.atomic():
            video_model = VideoModelMapper.to_model(video)
            self._save_medias(video_model)
            video_model.save()
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

    def get_by_id(self, id: UUID) -> Video | None:
        try:
            video_model = VideoORM.objects.get(id=id)
        except VideoORM.DoesNotExist:
            return None
        else:
            return VideoModelMapper.to_entity(video_model)

    def delete(self, id: UUID) -> None:
        VideoORM.objects.filter(id=id).delete()

    def list(self) -> list[Video]:
        return [VideoModelMapper.to_entity(video) for video in VideoORM.objects.all()]

    def update(self, video: Video) -> None:
        try:
            video_model = VideoORM.objects.get(pk=video.id)
        except VideoORM.DoesNotExist:
            return None

        with transaction.atomic():
            # Remove related medias - if they exist
            self._delete_medias(video_model=video_model)

            # Persist related medias if they exist in the entity
            video_model.banner = VideoModelMapper.image_to_model(video.banner)
            video_model.thumbnail = VideoModelMapper.image_to_model(video.thumbnail)
            video_model.thumbnail_half = VideoModelMapper.image_to_model(video.thumbnail_half)
            video_model.trailer = VideoModelMapper.audio_video_to_model(video.trailer)
            video_model.video = VideoModelMapper.audio_video_to_model(video.video)
            self._save_medias(video_model)

            # Update relationships with other entities/aggregates
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

            # Update video attributes
            video_model.title = video.title
            video_model.description = video.description
            video_model.launch_year = video.launch_year
            video_model.opened = video.opened
            video_model.duration = video.duration
            video_model.rating = video.rating
            video_model.published = video.published

            video_model.save()

class VideoModelMapper:
    @staticmethod
    def image_to_model(media: ImageMedia | None) -> ImageMediaORM | None:
        if not media:
            return None

        return ImageMediaORM(
            name=media.name,
            raw_location=media.location,
            checksum="",
        )

    @staticmethod
    def audio_video_to_model(media: AudioVideoMedia | None) -> AudioVideoMediaORM | None:
        if media is None:
            return None
        return AudioVideoMediaORM(
            name=media.name,
            raw_location=media.raw_location,
            encoded_location=media.encoded_location,
            status=media.status.value,
            checksum="",
        )

    @staticmethod
    def image_to_entity(
        image_model: ImageMediaORM | None
    ) -> ImageMedia | None:
        if not image_model:
            return None

        return ImageMedia(
            name=image_model.name,
            location=image_model.raw_location,
        )

    @staticmethod
    def audio_video_to_entity(
        audio_video_model: AudioVideoMediaORM | None
    ) -> AudioVideoMedia | None:
        if not audio_video_model:
            return None

        return AudioVideoMedia(
            name=audio_video_model.name,
            raw_location=audio_video_model.raw_location,
            encoded_location=audio_video_model.encoded_location,
            status=MediaStatus(audio_video_model.status),
        )

    @staticmethod
    def to_entity(model: VideoORM) -> Video:
        rating = model.rating

        if not isinstance(rating, Rating):
            if "Rating" in rating:
                rating = Rating(rating.split(".")[-1])
            else:
                rating = Rating(rating)

        video = Video(
            id=model.id,
            title=model.title,
            description=model.description,
            launch_year=model.launch_year,
            opened=model.opened,
            duration=model.duration,
            rating=rating,
            categories=set(model.categories.values_list("id", flat=True)),
            genres=set(model.genres.values_list("id", flat=True)),
            cast_members=set(model.cast_members.values_list("id", flat=True)),
        )

        video.banner = VideoModelMapper.image_to_entity(
            image_model=model.banner
        )
        video.thumbnail = VideoModelMapper.image_to_entity(
            image_model=model.thumbnail
        )
        video.thumbnail_half = VideoModelMapper.image_to_entity(
            image_model=model.thumbnail_half
        )
        video.trailer = VideoModelMapper.audio_video_to_entity(
            audio_video_model=model.trailer
        )
        video.video = VideoModelMapper.audio_video_to_entity(
            audio_video_model=model.video
        )

        return video

    @staticmethod
    def to_model(video: Video) -> VideoORM:
        return VideoORM(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            opened=video.opened,
            duration=video.duration,
            rating=video.rating.value,
            published=video.published,
            banner=VideoModelMapper.image_to_model(video.banner),
            thumbnail=VideoModelMapper.image_to_model(video.thumbnail),
            thumbnail_half=VideoModelMapper.image_to_model(video.thumbnail_half),
            trailer=VideoModelMapper.audio_video_to_model(video.trailer),
            video=VideoModelMapper.audio_video_to_model(video.video),
        )
