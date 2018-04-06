from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.client.models import Transport
from apps.info.models import City, Country, TransportType, TransportMark, TransportModel, TransportBody, \
    TransportShippingType, Region
from apps.info.serializers import CitySerializer, CountrySerializer, TransportTypeSerializer, TransportMarkSerializer, \
    TransportModelSerializer, TransportBodySerializer, TransportShippingTypeSerializer, RegionSerializer


class CityViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_fields = ('mark',)


class RegionViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    filter_fields = ('country',)


class CountryViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class TransportTypeViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = TransportTypeSerializer
    queryset = TransportType.objects.all()


class TransportMarkViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = TransportMarkSerializer
    queryset = TransportMark.objects.all()


class TransportModelViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = TransportModelSerializer
    queryset = TransportModel.objects.all()
    filter_fields = ('mark',)


class TransportBodyViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = TransportBodySerializer
    queryset = TransportBody.objects.all()


class TransportShippingTypeViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = TransportShippingTypeSerializer
    queryset = TransportShippingType.objects.all()
