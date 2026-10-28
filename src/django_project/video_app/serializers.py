from rest_framework import serializers

from src.django_project.shared.serializers import (
    IdSerializer,
    SetField,
    ListResponseSerializer,
)


class CreateVideoWithoutMediaInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    opened = serializers.BooleanField()
    rating = serializers.CharField(max_length=255)
    duration = serializers.DecimalField(max_digits=10, decimal_places=2)
    categories = SetField(child=serializers.UUIDField())
    genres = SetField(child=serializers.UUIDField())
    cast_members = SetField(child=serializers.UUIDField())


class CreateVideoWithoutMediaOutputSerializer(IdSerializer):
    pass


class ImageMediaOutputSerializer(serializers.Serializer):
    name = serializers.CharField()
    location = serializers.CharField()


class AudioVideoMediaOutputSerializer(serializers.Serializer):
    name = serializers.CharField()
    raw_location = serializers.CharField()
    encoded_location = serializers.CharField()
    status = serializers.CharField(source="status.value")


class VideoOutputSerializer(IdSerializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1024)
    launch_year = serializers.IntegerField()
    duration = serializers.DecimalField(max_digits=10, decimal_places=2)
    rating = serializers.CharField(source="rating.value")
    opened = serializers.BooleanField()
    published = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())
    genres = serializers.ListField(child=serializers.UUIDField())
    cast_members = serializers.ListField(child=serializers.UUIDField())
    banner = ImageMediaOutputSerializer(allow_null=True)
    thumbnail = ImageMediaOutputSerializer(allow_null=True)
    thumbnail_half = ImageMediaOutputSerializer(allow_null=True)
    trailer = AudioVideoMediaOutputSerializer(allow_null=True)
    video = AudioVideoMediaOutputSerializer(allow_null=True)


class ListVideoOutputSerializer(ListResponseSerializer):
    data = VideoOutputSerializer(many=True)
