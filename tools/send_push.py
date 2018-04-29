# coding=utf-8
from push_notifications.models import APNSDevice

queryset = APNSDevice.objects.all()
print(len(queryset))
clients = queryset.filter(user__type='clients')
couriers = queryset.filter(user__type='courier')

print(len(clients))
print(len(couriers))

clients.send_message(
    content_available=1, extra={
        "boo": "foo"
    }, message={
        "title": "Клиент оформил заказ",
        "body": "Hello client"
    },
    thread_id="123", sound='chime.aiff')

couriers.send_message(
    content_available=1, extra={
        "boo": "foo"
    }, message={
        "title": "Клиент оформил заказ",
        "body": "Hello courier"
    },
    thread_id="123", sound='chime.aiff')
