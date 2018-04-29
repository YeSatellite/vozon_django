# coding=utf-8
from django.db.models.signals import post_save
from django.dispatch import receiver
from push_notifications.models import APNSDevice

from apps.client.models import Order
from apps.client.serializers import OrderSerializer


@receiver(post_save, sender=Order)
def save_profile(sender, instance, **kwargs):
    """
    :type instance: Order
    """
    serializer = OrderSerializer(instance)

    APNSDevice.objects.filter(owner__type='courier',
                              owner__city=instance.start_point).send_message(
        content_available=1, extra={
            serializer.data
        }, message={
            "title": "Клиент оформил заказ",
            "body": instance.title
        },
        thread_id="123", sound='chime.aiff')
