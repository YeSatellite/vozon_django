# coding=utf-8
from django.db import models
from rest_framework.exceptions import ValidationError

from apps.core.models import TimeStampedMixin, SoftDeletionMixin
from apps.info.models import City, TransportType, TransportModel, TransportBody, TransportShippingType, PaymentType, \
    OtherService, Category
from apps.user.models import User


class Transport(TimeStampedMixin,
                SoftDeletionMixin):
    owner = models.ForeignKey(User, models.CASCADE, related_name='transport')

    type = models.ForeignKey(TransportType, models.CASCADE)
    model = models.ForeignKey(TransportModel, models.CASCADE)
    body = models.ForeignKey(TransportBody, models.CASCADE)
    shipping_type = models.ForeignKey(TransportShippingType, models.CASCADE)

    image1 = models.ImageField(upload_to='transport/', null=True)
    image2 = models.ImageField(upload_to='transport/', null=True)
    number = models.TextField()
    volume = models.FloatField()
    comment = models.CharField(max_length=100)


class Order(TimeStampedMixin):
    owner = models.ForeignKey(User, models.CASCADE, related_name='order_owner')

    title = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)

    start_point = models.ForeignKey(City, models.CASCADE, related_name='order_start_point')
    end_point = models.ForeignKey(City, models.CASCADE, related_name='order_end_point')
    start_detail = models.CharField(max_length=100)
    end_detail = models.CharField(max_length=100)

    volume = models.FloatField()
    mass = models.FloatField()

    image1 = models.ImageField(upload_to='cargo/', null=True)
    image2 = models.ImageField(upload_to='cargo/', null=True)

    owner_type = models.IntegerField()
    payment_type = models.ForeignKey(PaymentType, models.CASCADE)
    category = models.ForeignKey(Category, models.CASCADE)

    accept_person = models.CharField(max_length=100)
    accept_person_contact = models.CharField(max_length=20)

    shipping_date = models.DateField()
    shipping_time = models.TimeField()

    offer = models.ForeignKey('Offer', models.CASCADE, null=True, related_name='order_active_offer')

    def to_active(self, offer):
        if self.offer is not None:
            raise ValidationError('client order status is not \'posted\'.')
        if offer.order != self:
            raise ValidationError({'transport_offer': ['offer is not to your order']})

        self.offer = offer
        self.save()

        Offer.objects.filter(order=self).exclude(pk=offer.pk).delete()

    def to_done(self, ration):
        if self.offer is None:
            raise ValidationError('client order status is not \'active\'.')

        self.offer.transport.owner.rating_add(ration)
        self.offer.delete()
        self.delete()

    def __str__(self):
        return "%s_%d" % (self.owner, self.id)


def status_test(value):
    if value.transport is not None:
        raise ValidationError('client order no longer available.')


class Offer(TimeStampedMixin):
    transport = models.ForeignKey(Transport, models.CASCADE)
    order = models.ForeignKey(Order, models.CASCADE, validators=[status_test], related_name='offer_order')

    price = models.PositiveIntegerField()

    payment_type = models.ForeignKey(PaymentType, models.CASCADE)
    other_service = models.ForeignKey(OtherService, models.CASCADE)
    shipping_type = models.ForeignKey(TransportShippingType, models.CASCADE)

    comment = models.CharField(max_length=1000)

    class Meta:
        unique_together = (("transport", "order"),)


class Route(TimeStampedMixin):
    owner = models.ForeignKey(User, models.CASCADE)
    transport = models.ForeignKey(Transport, models.CASCADE, related_name='route_transport', null=True)

    start_point = models.ForeignKey(City, models.CASCADE, related_name='route_start_point')
    end_point = models.ForeignKey(City, models.CASCADE, related_name='route_end_point')

    shipping_date = models.DateField()
    shipping_time = models.TimeField()
