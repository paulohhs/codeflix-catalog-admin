from uuid import UUID

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from src.core.category.application.usecases.exceptions import CategoryNotFound
from src.core.category.application.usecases.get_category import (
    GetCategory,
    GetCategoryRequest,
)
from src.core.category.application.usecases.list_category import (
    ListCategory,
    ListCategoryRequest,
)
from django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.serializers import (
    ListCategoryResponseSerializer, 
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer
)


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryRequest()

        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        response = use_case.execute(input)
     
        serializer = ListCategoryResponseSerializer(instance=response)

        return Response(
            status=HTTP_200_OK,
            data=serializer.data,
        )

    def retrieve(self, request: Request, pk=None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            result = use_case.execute(
                request=GetCategoryRequest(id=serializer.validated_data["id"])
            )
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_output = RetrieveCategoryResponseSerializer(instance=result)

        return Response(
            status=HTTP_200_OK,
            data=category_output.data
        )
