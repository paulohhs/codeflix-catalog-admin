from rest_framework import serializers

from src.core.cast_member.domain.cast_member import CastMemberType
from src.django_project.shared.serializers import ListResponseSerializer, IdSerializer


class CastMemberOutputSerializer(IdSerializer):
    name = serializers.CharField(max_length=255)
    type = serializers.ChoiceField(choices=[type.value for type in CastMemberType])


class ListCastMemberOutputSerializer(ListResponseSerializer):
    data = CastMemberOutputSerializer(many=True)


class CastMemberTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        # Utilizamos o "choices" do DRF, que permite um conjunto de opções limitado para um certo campo.
        choices = [(type.name, type.value) for type in CastMemberType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        # Valor vindo da API como "str" é convertido para o StrEnum
        return CastMemberType(super().to_internal_value(data))

    def to_representation(self, value):
        # O valor vindo do nosso domínio é convertido para uma string na API
        return str(super().to_representation(value))


class CreateCastMemberInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    type = CastMemberTypeField()


class CreateCastMemberOutputSerializer(IdSerializer):
    pass


class UpdateCastMemberInputSerializer(IdSerializer):
    name = serializers.CharField(required=True)
    type = CastMemberTypeField(required=True)


class DeleteCastMemberInputSerializer(IdSerializer):
    pass
