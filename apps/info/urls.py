from rest_framework.routers import DefaultRouter

from apps.info.views import CityViewSet, CountryViewSet, TransportTypeViewSet, TransportMarkViewSet, \
    TransportModelViewSet, TransportBodyViewSet, TransportShippingTypeViewSet, RegionViewSet, PaymentTypeViewSet, \
    OtherServiceViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'city', CityViewSet, base_name='city')
router.register(r'region', RegionViewSet, base_name='region')
router.register(r'country', CountryViewSet, base_name='location')
router.register(r'transport/type', TransportTypeViewSet, base_name='transport type')
router.register(r'transport/mark', TransportMarkViewSet, base_name='transport mark')
router.register(r'transport/model', TransportModelViewSet, base_name='transport model')
router.register(r'transport/body', TransportBodyViewSet, base_name='transport body')
router.register(r'transport/shipping-type', TransportShippingTypeViewSet, base_name='transport shipping type')
router.register(r'payment-type', PaymentTypeViewSet, base_name='payment type')
router.register(r'other-type', OtherServiceViewSet, base_name='other type')
router.register(r'category', CategoryViewSet, base_name='category')

urlpatterns = router.urls
