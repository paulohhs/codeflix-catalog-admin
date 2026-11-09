import pytest

from src.core.video.domain.value_objects import MediaStatus, MediaType, AudioVideoMedia
from src.core.video.application.use_cases.process_audio_video_media import ProcessAudioVideoMedia


class TestProcessAudioVideoMedia:
    @pytest.mark.parametrize(
        "media_type", [
            MediaType.BANNER,
            MediaType.THUMBNAIL,
        ]
    )
    def test_process_video_with_invalid_media_type_request(
        self,
        mock_video_without_association,
        mock_im_video_repository,
        media_type,
    ):
        video = mock_video_without_association
        media = AudioVideoMedia(
            name="video.mp4",
            raw_location="raw_path",
            encoded_location="encoded_path",
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        video.video = media
        mock_im_video_repository.videos = [video]
        input = ProcessAudioVideoMedia.Input(
            encoded_location="encoded_location_test",
            video_id=video.id,
            status=MediaStatus.COMPLETED,
            media_type=media_type,
        )

        use_case = ProcessAudioVideoMedia(
            video_repository=mock_im_video_repository
        )

        with pytest.raises(ValueError, match="The media type must be VIDEO or TRAILER"):
            use_case.execute(request=input)

    def test_process_audio_video_media_complete_and_publish(
        self,
        mock_video_without_association,
        mock_im_video_repository,
    ):
        original_encoded_location = "encoded_path"

        video = mock_video_without_association
        media = AudioVideoMedia(
            name="video.mp4",
            raw_location="raw_path",
            encoded_location=original_encoded_location,
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        video.video = media
        mock_im_video_repository.videos = [video]
        input = ProcessAudioVideoMedia.Input(
            encoded_location="encoded_location_test",
            video_id=video.id,
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )

        use_case = ProcessAudioVideoMedia(
            video_repository=mock_im_video_repository
        )
        use_case.execute(request=input)

        video_from_repo = mock_im_video_repository.get_by_id(video.id)
        assert video_from_repo.video.status == MediaStatus.COMPLETED
        assert video_from_repo.video.encoded_location != original_encoded_location
        assert video_from_repo.video.encoded_location == "encoded_location_test"
        assert video_from_repo.published is True

    def test_process_audio_video_media_fail(
        self,
        mock_video_without_association,
        mock_im_video_repository,
    ):
        original_encoded_location = "encoded_path"

        video = mock_video_without_association
        media = AudioVideoMedia(
            name="video.mp4",
            raw_location="raw_path",
            encoded_location=original_encoded_location,
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        video.video = media
        mock_im_video_repository.videos = [video]

        input = ProcessAudioVideoMedia.Input(
            encoded_location="encoded_location_test",
            video_id=video.id,
            status=MediaStatus.PROCESSING,
            media_type=MediaType.VIDEO,
        )

        use_case = ProcessAudioVideoMedia(
            video_repository=mock_im_video_repository
        )
        use_case.execute(request=input)

        video_from_repo = mock_im_video_repository.get_by_id(video.id)
        assert video_from_repo.video.status == MediaStatus.ERROR
        assert video_from_repo.video.encoded_location == original_encoded_location
        assert video_from_repo.published is False
