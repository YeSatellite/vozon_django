from rest_framework.routers import DefaultRouter

from apps.info.views import CityViewSet, CountryViewSet, TransportTypeViewSet, TransportMarkViewSet, \
    TransportModelViewSet, TransportBodyViewSet, TransportShippingTypeViewSet

router = DefaultRouter()
router.register(r'city', CityViewSet, base_name='city')
router.register(r'country', CountryViewSet, base_name='location')
router.register(r'transport/type', TransportTypeViewSet, base_name='transport type')
router.register(r'transport/mark', TransportMarkViewSet, base_name='transport mark')
router.register(r'transport/model', TransportModelViewSet, base_name='transport model')
router.register(r'transport/body', TransportBodyViewSet, base_name='transport body')
router.register(r'transport/shipping-type', TransportShippingTypeViewSet, base_name='transport shipping type')

urlpatterns = router.urls
