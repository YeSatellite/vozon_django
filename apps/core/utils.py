# coding=utf-8
import json
import logging

import requests
from django.conf import settings
from push_notifications.models import APNSDevice
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

norm = logging.getLogger('project.need').debug


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
    login = getattr(settings, 'SMS_LOGIN', None)
    assert login is not None

    password = getattr(settings, 'SMS_PASSWORD', None)
    assert password is not None

    message = 'VozON: %s' % message

    payload = {
        "login": login,
        "password": password,
        "messages": [{
            "phone": phone,
            "clientId": "1",
            "text": message
        }]
    }

    r = requests.post('http://api.prostor-sms.ru/messages/v2/send.json', json=payload)

    print(r.text)
    data = json.loads(r.text)

    status = data.get('status', "tmp")

    if status != 'ok':
        raise ValidationError({"sms": ["server error"]})

    status = data['messages'][0].get('status', 'unknown error')
    if status != 'accepted':
        raise ValidationError({"sms": status})

    norm(phone + "@" + message)
    norm(">>>" + str(data) + "<<<")
