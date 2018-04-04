# coding=utf-8
from rest_framework import serializers

from apps.info.serializers import CitySerializer
from apps.user.manager import TYPE
from apps.user.models import User

USER_CLIENT_FIELDS = ('id', 'phone', 'name', 'city', 'citizenship', 'dob')
USER_COURIER_FIELDS = USER_CLIENT_FIELDS + ('avatar', 'experience', 'rating',)


class ClientRegisterSerializer(serializers.ModelSerializer):
    type = TYPE[0][0]

    def create(self, validated_data):
        validated_data['type'] = self.type
        return super().create(validated_data)

    class Meta:
        model = User
        fields = USER_CLIENT_FIELDS


class ClientSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = User
        fields = USER_CLIENT_FIELDS


class CourierRegisterSerializer(ClientRegisterSerializer):
    type = TYPE[1][1]

    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        if obj.rating_count == 0:
            return -1
        return obj.rating_sum/obj.rating_count

    class Meta:
        model = User
        fields = USER_COURIER_FIELDS


class CourierSerializer(CourierRegisterSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = User
        fields = USER_COURIER_FIELDS
