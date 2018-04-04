# coding=utf-8
from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.user.views import ClientRegisterAPIView, login, sent_sms, CourierRegisterAPIView
from .views import ClientViewSet, ClientOrderViewSet, CourierViewSet, CourierOrderViewSet, TransportViewSet, \
    CourierOfferViewSet

client_router = DefaultRouter()
client_router.register(r'clients', ClientViewSet, base_name='client')
client_router.register(r'order', ClientOrderViewSet, base_name='order')

client = [
    url(r'register/', ClientRegisterAPIView.as_view()),
    url(r'login/', login),
    url(r'sent-sms/', sent_sms),
]
client += client_router.urls

#  ---------------------------------------


courier_router = DefaultRouter()
courier_router.register(r'couriers', CourierViewSet, base_name='courier')
courier_router.register(r'order', CourierOrderViewSet, base_name='order')
courier_router.register(r'transports', TransportViewSet, base_name='transport')
courier_router.register(r'order/(?P<order>\d+)/offer', CourierOfferViewSet, base_name='offer')

courier = [
    url(r'register/', CourierRegisterAPIView.as_view()),
    url(r'login/', login),
    url(r'sent-sms/', sent_sms),
]
courier += courier_router.urls

urlpatterns = [
    path('client/', include(client)),
    path('courier/', include(courier)),
]
