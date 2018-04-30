# coding=utf-8
import json
import logging

import requests
from django.conf import settings
from push_notifications.models import APNSDevice
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

norm = logging.getLogger('project.need')


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    error_code = getattr(settings, 'ERROR_CODE', None)
    assert isinstance(error_code, dict)
    if isinstance(exc, exceptions.APIException):
        if isinstance(exc.detail, dict):
            r_error_code = 100
            for key, value in error_code.items():
                if isinstance(key, str):
                    field = key
                    message = None
                elif isinstance(key, (list, tuple)):
                    assert len(key) == 2
                    assert isinstance(key[0], str)
                    assert isinstance(key[1], str)
                    field = key[0]
                    message = key[1]
                else:
                    raise AssertionError('key error')

                exc_message = exc.detail.get(field, None)
                if not exc_message:
                    continue

                if message is None or (message in exc_message):
                    r_error_code = value
                    break
            response['Error-Code'] = r_error_code

    return response


def sms_sender(phone, message):
    login = getattr(settings, 'SMSC_LOGIN', None)
    assert login is not None

    password = getattr(settings, 'SMSC_PASSWORD', None)
    assert password is not None

    message = 'Vozon\n Ваш код подтверждения\n %s' % message

    payload = {
        'login': login,
        'psw': password,
        'phones': phone,
        'mes': message,
        'fmt': 3,
        # 'cost': '1',
    }
    r = requests.get('https://smsc.kz/sys/send.php', params=payload)

    print(r.text)
    data = json.loads(r.text)

    error_code = int(data.get('error_code', -1))

    if error_code in [1, 2, 3, 4, 5, 6, 8, 9]:
        raise ValidationError({"sms": ["server error"]})

    if error_code in [7]:
        raise ValidationError({"sms": ["number do not exist"]})

    norm.debug(phone + "@" + message)
    norm.debug(data)


def send_notification(title, body, action, **kwargs):
    norm.debug(APNSDevice.objects.filter(**kwargs))

    APNSDevice.objects.filter(**kwargs).send_message(
        content_available=1, extra={
            'action': action
        }
        , message={
            "title": title,
            "body": body
        },
        thread_id="123", sound='chime.aiff')
