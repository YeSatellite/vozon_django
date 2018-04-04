# coding=utf-8
from rest_framework import serializers

from apps.info.models import City, TransportType, Country, TransportMark, TransportModel, TransportBody, \
    TransportShippingType


class CitySerializer(serializers.ModelSerializer):
    country = serializers.ReadOnlyField(source='region.country.name')
    region = serializers.ReadOnlyField(source='region.name')

    class Meta:
        model = City
        fields = ('id', 'name', 'region', 'country')
        read_only_fields = ('name', 'region', 'country')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name',)


class TransportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportType
        fields = ('id', 'name')


class TransportMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportMark
        fields = ('id', 'name')


class TransportModelSerializer(serializers.ModelSerializer):
    mark_name = serializers.ReadOnlyField(source='mark.name')

    class Meta:
        model = TransportModel
        fields = ('id', 'name', 'mark', 'mark_name')


class TransportBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportBody
        fields = ('id', 'name')


class TransportShippingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportShippingType
        fields = ('id', 'name')
