# coding=utf-8
from rest_framework import serializers

from apps.info.models import City, TransportType, Country, TransportMark, TransportModel, TransportBody, \
    TransportShippingType, Region, PaymentType, OtherService, Category


class CitySerializer(serializers.ModelSerializer):
    region_name = serializers.ReadOnlyField(source='region.name')
    country_name = serializers.ReadOnlyField(source='region.country.name')

    class Meta:
        model = City
        fields = ('id', 'name', 'region_name', 'country_name')


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name', 'country')


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


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ('id', 'name')


class OtherServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherService
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'icon')
