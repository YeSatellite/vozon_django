# coding=utf-8
from rest_framework import serializers

from apps.client.models import Transport, Order, Offer
from apps.core.serializers import UserOwnerMixin
from apps.info.serializers import CitySerializer, TransportTypeSerializer
from apps.user.models import User

USER_CLIENT_FIELDS = ('id', 'phone', 'name', 'city', 'citizenship', 'dob')
USER_COURIER_FIELDS = USER_CLIENT_FIELDS + \
                      ('avatar', 'experience', 'raring_sum', 'raring_count')


class ClientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = USER_CLIENT_FIELDS


class ClientSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = User
        fields = USER_CLIENT_FIELDS


class CourierRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = USER_COURIER_FIELDS


class CourierSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = User
        fields = USER_COURIER_FIELDS


# -------------------------------------------

TRANSPORT_FIELDS = ('id', 'owner', 'type', 'image1', 'image2', 'modification', 'number', 'volume', 'comment',
                    'type_id')


class TransportSerializer(serializers.ModelSerializer, UserOwnerMixin):
    owner = CourierSerializer(read_only=True)
    type = TransportTypeSerializer(read_only=True)

    class Meta:
        model = Transport
        fields = TRANSPORT_FIELDS


# -------------------------------------------


ORDER_FIELDS = ('id', 'owner',
                'title', 'comment',
                'start_point', 'end_point', 'start_detail', 'end_detail',
                'volume', 'mass',
                'image1', 'image2',
                'owner_type', 'payment_type',
                'accept_person', 'accept_person_contact',
                'transport', 'price',
                'start_point_id', 'end_point_id', 'transport_id')


class OrderSerializer(serializers.ModelSerializer, UserOwnerMixin):
    owner = ClientSerializer(read_only=True)

    start_point = CitySerializer(read_only=True)
    end_point = CitySerializer(read_only=True)
    transport = TransportSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ORDER_FIELDS


TRANSPORT_OFFER_FIELDS = ('id', 'transport', 'order', 'price', 'extra_info',
                          'transport_id')


class OfferSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = TRANSPORT_OFFER_FIELDS

    def validate(self, attrs):
        transport = attrs['transport_id']
        client_order = attrs['order']

        transport = Transport.objects.get(pk=transport)
        user = self.context['request'].user
        if transport.owner != user:
            raise serializers.ValidationError("it is not your transport")

        try:
            Offer.objects.get(transport=transport, client_order=client_order)
        except Offer.DoesNotExist:
            return attrs
        raise serializers.ValidationError('transport with client_order already exists')
