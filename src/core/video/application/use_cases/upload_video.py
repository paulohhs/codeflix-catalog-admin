from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core.video.domain.value_objects import MediaType
from src.core._shared.infrastructure.storage.abstract_storage_service import (
    AbstractStorageService,
)
from src.core.video.domain.value_objects import MediaStatus
from src.core.video.domain.value_objects import AudioVideoMedia
from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.domain.repository import VideoRepository


class UploadVideo:
    @dataclass
    class Input:
        video_id: UUID
        file_name: str
        content: bytes
        content_type: str

    def __init__(
        self,
        video_repository: VideoRepository,
        storage_service: AbstractStorageService,
        message_bus: AbstractMessageBus,
    ) -> None:
        self.video_repository = video_repository
        self.storage_service = storage_service
        self.message_bus = message_bus

    def execute(self, input: Input) -> None:
        video = self.video_repository.get_by_id(input.video_id)
        if video is None:
            raise VideoNotFound(input.video_id)

        file_path = Path("videos") / str(video.id) / input.file_name
        self.storage_service.store(
            file_path=str(file_path),
            content=input.content,
            content_type=input.content_type
        )

        audio_video_media = AudioVideoMedia(
            name=input.file_name,
            raw_location=str(file_path),
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO,
        )
        video.update_video_media(audio_video_media)

        self.video_repository.update(video)
        self.message_bus.handle([
            AudioVideoMediaUpdatedIntegrationEvent(
                resource_id=f"{video.id}.{MediaType.VIDEO}",
                file_path=str(file_path),
            )
        ])
