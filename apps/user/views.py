# coding=utf-8
import datetime
import logging

import jwt
from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.db.models import Q
from django.utils.timezone import utc
from push_notifications.models import APNSDevice
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler

from apps.user.serializers import RegisterSerializer, UserSerializer
from .manager import TYPE
from .models import User


class RegisterAPIView(CreateModelMixin,
                      GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    type = TYPE[0][0]

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        user = self.get_queryset().get(id=response.data['id'])
        user.send_sms_confirmation()
        return response


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    phone = request.data.get("phone")
    sms_code = request.data.get("sms_code")
    phone_type = request.data.get("phone_type")
    device_id = request.data.get("device_id")
    registration_id = request.data.get("registration_id")
    print(phone_type)

    try:
        user = User.objects.get(phone=phone)
    except:
        raise AuthenticationFailed({"phone": ["phone doesn't exist"]})
    if not user.sms_code:
        raise AuthenticationFailed({"sms": ["sms didn't send"]}, )
    if user.sms_code != sms_code:
        raise AuthenticationFailed({"sms": ["sms not correct"]})

    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    delta = now - user.modified
    if delta > datetime.timedelta(minutes=2):
        raise AuthenticationFailed({"sms": ["sms code expired"]})

    user.sms_code = None
    user.save()
    serializer = UserSerializer(user, context={"request": request})
    data = serializer.data

    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    update_last_login(None, user)
    data['token'] = token.decode('unicode_escape')

    logger = logging.getLogger('project.need')
    logger.debug("phone_type: "+phone_type)
    if phone_type == 'iOS':

        APNSDevice.objects.filter(Q(registration_id=registration_id) |
                                  Q(device_id=device_id) |
                                  Q(user=user)).delete()
        APNSDevice.objects.create(registration_id=registration_id, device_id=device_id, user=user)
    return Response(data)


@api_view(["POST"])
@permission_classes((AllowAny,))
def sent_sms(request):
    phone = request.data.get("phone")

    try:
        user = User.objects.get(phone=phone)
    except:
        raise AuthenticationFailed({"phone": ["phone doesn't exist"]})

    user.send_sms_confirmation()
    return Response({'status': 'sms successfully sent'})
