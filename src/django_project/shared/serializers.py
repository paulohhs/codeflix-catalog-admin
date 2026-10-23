from rest_framework import serializers
from typing import TypeVar, Generic


T = TypeVar("T")


class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()


class ListResponseSerializer(Generic[T], serializers.Serializer):
    data: T
    meta = ListOutputMetaSerializer()


class IdSerializer(serializers.Serializer):
    id = serializers.UUIDField()
