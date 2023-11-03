from rest_framework import serializers
from entities import models


class FederalEntity(serializers.ModelSerializer):
    class Meta:
        model = models.FederalEntity
        fields = [
            'key',
            'name',
            'code'
        ]


class Entity(serializers.ModelSerializer):
    federal_entity = serializers.ReadOnlyField()

    class Meta:
        model = models.Entity
        fields = [
            'zip_code',
            'locality',
            'federal_entity'
        ]
