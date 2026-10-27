from rest_framework import serializers

from src.django_project.shared.serializers import ListResponseSerializer, IdSerializer, SetField


class GenreOutputSerializer(IdSerializer):
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class ListGenreOutputSerializer(ListResponseSerializer):
    data = GenreOutputSerializer(many=True)
    

class CreateGenreInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField(default=True)
    categories = SetField(child=serializers.UUIDField())


class CreateGenreOutputSerializer(IdSerializer):
    pass


class UpdateGenreInputSerializer(IdSerializer):
    name = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=True)
    categories = SetField(child=serializers.UUIDField(), required=True, allow_empty=True)


class DeleteGenreInputSerializer(IdSerializer):
    pass
