from rest_framework import serializers

from src.django_project.shared.serializers import IdSerializer, SetField


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