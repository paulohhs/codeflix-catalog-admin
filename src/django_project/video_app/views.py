from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core._shared.infrastructure.storage.local_storage import LocalStorage
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.django_project.video_app.serializers import (
    CreateVideoWithoutMediaInputSerializer,
    CreateVideoWithoutMediaOutputSerializer,
)
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.application.use_cases.exceptions import (
    InvalidVideo,
    RelatedEntitiesNotFound,
)
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository


class VideoViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer = CreateVideoWithoutMediaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateVideoWithoutMedia.Input(**serializer.validated_data)
        use_case = CreateVideoWithoutMedia(
            video_repository=DjangoORMVideoRepository(),
            category_repository=DjangoORMCategoryRepository(),
            genre_repository=DjangoORMGenreRepository(),
            cast_member_repository=DjangoORMCastMemberRepository(),
        )

        try:
            output = use_case.execute(input=input)
        except (InvalidVideo, RelatedEntitiesNotFound) as err:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(err)}
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateVideoWithoutMediaOutputSerializer(instance=output).data,
        )

    def partial_update(self, request: Request, pk: UUID) -> Response:
        file = request.FILES["video_file"]
        content = file.read()
        content_type = file.content_type

        upload_video = UploadVideo(
            video_repository=DjangoORMVideoRepository(),
            storage_service=LocalStorage(),
        )

        try:
            upload_video.execute(
                input=UploadVideo.Input(
                    video_id=pk,
                    file_name=file.name,
                    content=content,
                    content_type=content_type,
                )
            )
        except VideoNotFound as err:
            return Response(
                status=HTTP_404_NOT_FOUND, data={"error": str(err)}
            )

        return Response(status=HTTP_204_NO_CONTENT)

    def list(self, request: Request) -> Response:
        raise NotImplementedError

    def update(self, request: Request, pk: UUID) -> Response:
        raise NotImplementedError

    def destroy(self, request: Request, pk: UUID) -> Response:
        raise NotImplementedError
