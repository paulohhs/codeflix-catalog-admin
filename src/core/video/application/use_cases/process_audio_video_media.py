from dataclasses import dataclass
from uuid import UUID

from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.domain.repository import VideoRepository
from src.core.video.domain.value_objects import MediaStatus, MediaType


class ProcessAudioVideoMedia:
    @dataclass
    class Input:
        encoded_location: str
        video_id: UUID
        status: MediaStatus
        media_type: MediaType

    def __init__(
        self,
        video_repository: VideoRepository
    ) -> None:
        self.video_repository = video_repository

    def execute(self, request: Input) -> None:
        video = self.video_repository.get_by_id(id=request.video_id)
        if video is None:
            raise VideoNotFound(f"Video with id {request.video_id} not found")

        video.validate_audio_video_media_to_process(
            media_type=request.media_type,
        )
        video.process(
            status=request.status,
            encoded_location=request.encoded_location,
            media_type=request.media_type,
        )

        self.video_repository.update(video)
