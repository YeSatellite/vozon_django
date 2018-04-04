import jwt
from django.conf import settings
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler

from apps.client.serializers import ClientSerializer
from .manager import TYPE
from .models import User
from .serializers import ClientRegisterSerializer, CourierRegisterSerializer


class ClientRegisterAPIView(CreateModelMixin,
                            GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ClientRegisterSerializer
    permission_classes = (AllowAny,)
    type = TYPE[0][0]

    def post(self, request, *args, **kwargs):
        print(request.data)
        response = self.create(request, *args, **kwargs)
        user = self.get_queryset().get(id=response.data['id'])
        user.send_sms_confirmation()
        return response


class CourierRegisterAPIView(ClientRegisterAPIView):
    serializer_class = CourierRegisterSerializer


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    phone = request.data.get("phone")
    sms_code = request.data.get("sms_code")

    try:
        user = User.objects.get(phone=phone)
    except:
        return Response({"phone": ["phone don't exit"]},
                        status=status.HTTP_401_UNAUTHORIZED)
    if not user.sms_code:
        return Response({"sms": ["sms didn't send"]},
                        status=status.HTTP_401_UNAUTHORIZED)
    if user.sms_code != sms_code:
        return Response({"sms": ["sms not correct"]},
                        status=status.HTTP_401_UNAUTHORIZED)
    user.sms_code = None
    user.save()
    serializer = ClientSerializer(user, context={"request": request})
    data = serializer.data

    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    update_last_login(None, user)
    data['token'] = token.decode('unicode_escape')
    return Response(data)


@api_view(["POST"])
@permission_classes((AllowAny,))
def sent_sms(request):
    phone = request.data.get("phone")

    try:
        user = User.objects.get(phone=phone)
    except:
        return Response([{"phone": "phone don't exit"}, ],
                        status=status.HTTP_401_UNAUTHORIZED)

    user.send_sms_confirmation()
    return Response({'status': 'sms successfully sent'})

