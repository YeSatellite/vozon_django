# coding=utf-8
from django.db.models import Q
from push_notifications.models import APNSDevice, GCMDevice

from apps.core.utils import norm


def register_push(phone_type, registration_id, user):
    if phone_type == 'iOS':
        APNSDevice.objects.filter(Q(registration_id=registration_id) |
                                  Q(user=user)).delete()

        norm("New iOs device: %s %s" % (registration_id, user))
        APNSDevice.objects.create(registration_id=registration_id, user=user)

    if phone_type == 'Android':
        GCMDevice.objects.filter(Q(registration_id=registration_id) |
                                 Q(user=user)).delete()

        norm("New Android device: %s %s" % (registration_id, user))
        GCMDevice.objects.create(registration_id=registration_id, cloud_message_type="FCM", user=user)


def send_notification(title, body, action, **kwargs):
    APNSDevice.objects.filter(**kwargs).send_message(
        content_available=1,
        extra={
            'action': action
        },
        message={
            "title": title,
            "body": body
        },
        thread_id="123", sound='chime.aiff')

    GCMDevice.objects.filter(**kwargs).send_message(
        body,
        title=title,
        extra={"action": action},
        badge=1)
