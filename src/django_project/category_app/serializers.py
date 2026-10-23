from rest_framework import serializers

from src.django_project.shared.serializers import ListResponseSerializer, IdSerializer


class CategoryResponseSerializer(IdSerializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ListCategoryResponseSerializer(ListResponseSerializer):
    data = CategoryResponseSerializer(many=True)


class RetrieveCategoryRequestSerializer(IdSerializer):
    pass


class RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(source="*")


class CreateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    is_active = serializers.BooleanField(default=True)


class CreateCategoryResponseSerializer(IdSerializer):
    pass


class UpdateCategoryRequestSerializer(IdSerializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class DeleteCategoryRequestSerializer(IdSerializer):
    pass
