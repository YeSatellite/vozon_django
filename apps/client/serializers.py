# coding=utf-8
from rest_framework import serializers

from apps.client.models import Transport, Order, Offer, Route
from apps.info.models import City
from apps.info.serializers import CitySerializer
from apps.user.serializers import UserSerializer

TRANSPORT_FIELDS = ('id', 'owner',
                    'type', 'model', 'body', 'shipping_type',
                    'type_name', 'mark_name', 'model_name', 'body_name', 'shipping_type_name',
                    'image1', 'image2', 'number', 'volume', 'comment')


class TransportSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    type_name = serializers.ReadOnlyField(source='type.name')
    mark_name = serializers.ReadOnlyField(source='model.mark.name')
    model_name = serializers.ReadOnlyField(source='model.name')
    body_name = serializers.ReadOnlyField(source='body.name')
    shipping_type_name = serializers.ReadOnlyField(source='shipping_type.name')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Transport
        fields = TRANSPORT_FIELDS


# -------------------------------------------

TRANSPORT_OFFER_FIELDS = ('id', 'transport', 'order', 'price',
                          'payment_type', 'other_service', 'shipping_type',
                          'payment_type_name', 'other_service_name', 'shipping_type_name',
                          'comment', 'created',
                          'transport_id',)


class OfferSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(read_only=True)
    transport_id = serializers.IntegerField(write_only=True)
    created = serializers.DateTimeField(format="%Y-%m-%d")

    payment_type_name = serializers.ReadOnlyField(source='payment_type.name')
    other_service_name = serializers.ReadOnlyField(source='other_service.name')
    shipping_type_name = serializers.ReadOnlyField(source='shipping_type.name')

    class Meta:
        model = Offer
        fields = TRANSPORT_OFFER_FIELDS
        read_only_fields = ('order',)

    def validate(self, attrs):
        transport = attrs['transport_id']

        transport = Transport.objects.get(pk=transport)
        user = self.context['request'].user
        if transport.owner != user:
            raise serializers.ValidationError("it is not your transport")

        return attrs


ORDER_FIELDS = ('id', 'owner',
                'title', 'comment',
                'start_point', 'end_point', 'start_detail', 'end_detail',
                'volume', 'mass',
                'image1', 'image2',
                'owner_type', 'payment_type', 'payment_type_name',
                'category', 'category_name',
                'accept_person', 'accept_person_contact',
                'shipping_date', 'shipping_time',
                'offer',
                'start_point_id', 'end_point_id',)


class OrderSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    offer = OfferSerializer(read_only=True)

    start_point = CitySerializer(read_only=True)
    end_point = CitySerializer(read_only=True)
    start_point_id = serializers.IntegerField(write_only=True)
    end_point_id = serializers.IntegerField(write_only=True)

    payment_type_name = serializers.ReadOnlyField(source='payment_type.name')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Order
        fields = ORDER_FIELDS
        read_only_fields = ('price',)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        city = City.objects
        validated_data['start_point'] = city.get(pk=validated_data['start_point_id'])
        validated_data['end_point'] = city.get(pk=validated_data['end_point_id'])
        print(validated_data)
        return super().create(validated_data)


ROUTE_FIELDS = ('id', 'owner', 'transport', 'transport_id',
                'start_point', 'end_point', 'start_point_id', 'end_point_id',
                'shipping_date', 'shipping_time')


class RouteSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(read_only=True)
    transport_id = serializers.IntegerField(write_only=True, required=False)

    owner = UserSerializer(read_only=True)

    start_point = CitySerializer(read_only=True)
    end_point = CitySerializer(read_only=True)
    start_point_id = serializers.IntegerField(write_only=True)
    end_point_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Route
        fields = ROUTE_FIELDS
        read_only_fields = ('price',)

    def validate(self, attrs):
        attrs['owner'] = self.context['request'].user
        transport_id = attrs.get('transport_id', -1)
        if transport_id is not -1:
            try:
                transport = Transport.objects.get(pk=transport_id)
                if transport.owner != attrs['owner']:
                    raise serializers.ValidationError({'transport_id': ["it is not your transport"]})
            except Transport.DoesNotExist:
                raise serializers.ValidationError({'transport_id': ["doesn't exist"]})
        else:
            transport = None
        attrs['transport'] = transport
        attrs['start_point'] = City.objects.get(pk=attrs['start_point_id'])
        attrs['end_point'] = City.objects.get(pk=attrs['end_point_id'])

        return attrs
