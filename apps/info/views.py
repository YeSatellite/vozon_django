# coding=utf-8
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.info.models import City, Country, TransportType, TransportMark, TransportModel, TransportBody, \
    TransportShippingType, Region, PaymentType, OtherService, Category, TransportLoadType
from apps.info.serializers import CitySerializer, CountrySerializer, TransportMarkSerializer, \
    TransportModelSerializer, TransportBodySerializer, TransportShippingTypeSerializer, RegionSerializer, \
    PaymentTypeSerializer, OtherServiceSerializer, CategorySerializer, CountryPhoneSerializer, TransportTypeSerializer, \
    TransportLoadTypeSerializer


class CityViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_fields = ('region',)


class RegionViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    filter_fields = ('country',)


class CountryViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class CountryPhoneViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CountryPhoneSerializer
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


class TransportLoadTypeViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = TransportLoadTypeSerializer
    queryset = TransportLoadType.objects.all()


class PaymentTypeViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PaymentTypeSerializer
    queryset = PaymentType.objects.all()


class OtherServiceViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = OtherServiceSerializer
    queryset = OtherService.objects.all()


class CategoryViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TermsView(TemplateView):
    template_name = 'termsofuse.html'
