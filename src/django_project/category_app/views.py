from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        return Response(
            status=HTTP_200_OK,
            data=[
                {
                    "id": "632469e0-d6f3-42b1-b349-e47ed1e79cc4",
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                }, 
                {
                    "id": "f0efc68b-28f5-48ae-9544-cd74a0991270",
                    "name": "Documentary",
                    "description": "Documentary description",
                    "is_active": True,
                },
            ]
        )
