# coding=utf-8
from rest_framework import serializers

from apps.info.models import City, TransportType


class CitySerializer(serializers.ModelSerializer):
    country = serializers.ReadOnlyField(source='region.country.name')
    region = serializers.ReadOnlyField(source='region.name')

    class Meta:
        model = City
        fields = ('id', 'name', 'region', 'country')
        read_only_fields = ('name', 'region', 'country')


class TransportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportType
        fields = ('id', 'name')
