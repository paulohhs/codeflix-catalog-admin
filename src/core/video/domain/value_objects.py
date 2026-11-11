from dataclasses import dataclass
from enum import Enum, unique, StrEnum
from uuid import UUID


@dataclass(frozen=True)
class ImageMedia:
    name: str
    raw_location: str


@unique
class MediaStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


@unique
class Rating(Enum):
    ER = "ER"
    L = "L"
    AGE_10 = "AGE_10"
    AGE_12 = "AGE_12"
    AGE_14 = "AGE_14"
    AGE_16 = "AGE_16"
    AGE_18 = "AGE_18"


@unique
class MediaType(StrEnum):
    VIDEO = "VIDEO"
    TRAILER = "TRAILER"
    BANNER = "BANNER"
    THUMBNAIL = "THUMBNAIL"
    THUMBNAIL_HALF = "THUMBNAIL_HALF"


@dataclass(frozen=True)
class AudioVideoMedia:
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus
    media_type: MediaType

    def complete(self, encoded_location: str):
        return AudioVideoMedia(
            name=self.name,
            raw_location=self.raw_location,
            encoded_location=encoded_location,
            status=MediaStatus.COMPLETED,
            media_type=self.media_type,
        )

    def fail(self):
        return AudioVideoMedia(
            name=self.name,
            raw_location=self.raw_location,
            encoded_location=self.encoded_location,
            status=MediaStatus.ERROR,
            media_type=self.media_type,
        )
