# coding=utf-8
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import login, RegisterAPIView, sent_sms, ClientViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet, base_name='client')

urlpatterns = [
    url(r'register/', RegisterAPIView.as_view()),
    url(r'login/', login),
    url(r'sent-sms/', sent_sms),
]

urlpatterns += router.urls
