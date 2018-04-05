# coding=utf-8
from rest_framework import serializers

from apps.info.serializers import CitySerializer
from apps.user.manager import TYPE
from apps.user.models import User

USER_FIELDS = ('id', 'phone', 'name', 'city', 'citizenship', 'dob', 'type', 'avatar', 'experience', 'rating')


class RegisterSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        if obj.rating_count == 0:
            return -1
        return obj.rating_sum / obj.rating_count

    class Meta:
        model = User
        fields = USER_FIELDS


class UserSerializer(RegisterSerializer):
    city = CitySerializer(read_only=True)
