# coding=utf-8
from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet, ClientOrderViewSet, CourierViewSet, CourierOrderViewSet, TransportViewSet, \
    CourierOfferViewSet

client_router = DefaultRouter()
client_router.register(r'clients', ClientViewSet, base_name='client')
client_router.register(r'order', ClientOrderViewSet, base_name='order')


#  ---------------------------------------


courier_router = DefaultRouter()
courier_router.register(r'couriers', CourierViewSet, base_name='courier')
courier_router.register(r'order', CourierOrderViewSet, base_name='order')
courier_router.register(r'transports', TransportViewSet, base_name='transport')
courier_router.register(r'order/(?P<order>\d+)/offer', CourierOfferViewSet, base_name='offer')


urlpatterns = [
    url(r'^client/', include((client_router.urls, 'client'), namespace='client')),
    url(r'^courier/', include((courier_router.urls, 'courier'), namespace='courier'))
]
