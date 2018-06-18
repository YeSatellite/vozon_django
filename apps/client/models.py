# coding=utf-8
from django.db import models
from push_notifications.models import APNSDevice
from rest_framework.exceptions import ValidationError

from apps.core.models import TimeStampedMixin, SoftDeletionMixin
from apps.info.models import City, TransportType, TransportModel, TransportBody, PaymentType, \
    OtherService, TransportLoadType
from apps.user.models import User

PRICE_TYPE = (
    ('₸', '₸'),
    ('₽', '₽'),
    ('$', '$'),
    ('⊆', '⊆'),
)


class Transport(TimeStampedMixin):
    owner = models.ForeignKey(User, models.CASCADE, related_name='transport')

    model = models.ForeignKey(TransportModel, models.CASCADE)
    type = models.ForeignKey(TransportType, models.CASCADE)
    load_type = models.ForeignKey(TransportLoadType, models.CASCADE)

    image1 = models.ImageField(upload_to='transport/', null=True)
    image2 = models.ImageField(upload_to='transport/', null=True)
    number = models.TextField()
    width = models.FloatField()
    height = models.FloatField()
    length = models.FloatField()
    comment = models.CharField(max_length=100, blank=True)


class Order(TimeStampedMixin):
    owner = models.ForeignKey(User, models.CASCADE, related_name='order_owner')

    category_id = models.IntegerField()
    category = models.IntegerField()

    title = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)

    start_point = models.ForeignKey(City, models.CASCADE, related_name='order_start_point')
    end_point = models.ForeignKey(City, models.CASCADE, related_name='order_end_point')
    start_detail = models.CharField(max_length=100)
    end_detail = models.CharField(max_length=100)

    width = models.FloatField()
    height = models.FloatField()
    length = models.FloatField()
    mass = models.FloatField()

    image1 = models.ImageField(upload_to='cargo/', null=True)
    image2 = models.ImageField(upload_to='cargo/', null=True)

    payment_type = models.ForeignKey(PaymentType, models.CASCADE)
    type = models.ForeignKey(TransportType, models.CASCADE)

    accept_person = models.CharField(max_length=100)
    accept_person_contact = models.CharField(max_length=20)

    shipping_date = models.DateField()
    shipping_time = models.TimeField()

    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, choices=PRICE_TYPE)

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
    currency = models.CharField(max_length=10, choices=PRICE_TYPE)

    payment_type = models.ForeignKey(PaymentType, models.CASCADE)
    other_service = models.ForeignKey(OtherService, models.CASCADE)

    have_loaders = models.BooleanField()

    comment = models.CharField(max_length=1000)

    class Meta:
        unique_together = (("transport", "order"),)


class Route(TimeStampedMixin):
    owner = models.ForeignKey(User, models.CASCADE)
    transport = models.ForeignKey(Transport, models.CASCADE, related_name='route_transport')

    start_point = models.ForeignKey(City, models.CASCADE, related_name='route_start_point')
    end_point = models.ForeignKey(City, models.CASCADE, related_name='route_end_point', null=True)

    shipping_date = models.DateField()
    shipping_time = models.TimeField()

    comment = models.CharField(max_length=1000, blank=True)
