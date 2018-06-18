# coding=utf-8
from django.conf.urls import url

from apps.user.views import login, sent_sms, RegisterAPIView, remove_user

urlpatterns = [
    url(r'register/', RegisterAPIView.as_view()),
    url(r'login/', login),
    url(r'sent-sms/', sent_sms),
    url(r'remove-user/', remove_user),
]
