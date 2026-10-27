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


class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, data):
        return list(super().to_representation(data))
