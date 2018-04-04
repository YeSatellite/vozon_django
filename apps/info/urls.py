from rest_framework.routers import DefaultRouter

from apps.info.views import CityViewSet, CountryViewSet, TransportTypeViewSet, TransportMarkViewSet, \
    TransportModelViewSet, TransportBodyViewSet, TransportShippingTypeViewSet

router = DefaultRouter()
router.register(r'city', CityViewSet, base_name='city')
router.register(r'country', CountryViewSet, base_name='location')
router.register(r'transport/type', TransportTypeViewSet, base_name='transport_type')
router.register(r'transport/mark', TransportMarkViewSet, base_name='transport_mark')
router.register(r'transport/model', TransportModelViewSet, base_name='transport_model')
router.register(r'transport/body', TransportBodyViewSet, base_name='transport_body')
router.register(r'transport/shipping_type', TransportShippingTypeViewSet, base_name='transport_shipping_type')

urlpatterns = router.urls
