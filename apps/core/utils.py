# coding=utf-8
from django.conf import settings
from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    error_code = getattr(settings, 'ERROR_CODE', None)
    if response and error_code:
        response.status_code = status.HTTP_400_BAD_REQUEST
        assert isinstance(error_code, dict)
        for key, value in error_code.items():
            if isinstance(key, str):
                field = key
                message = None
            elif isinstance(key, list):
                assert len(key) == 2
                assert isinstance(key[0], str)
                assert isinstance(key[1], str)
                field = key[0]
                message = key[1]
            else:
                raise AssertionError('key error')

        response.data['status_code'] = response.status_code
    return response
