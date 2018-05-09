# coding=utf-8
from rest_framework import serializers

from apps.info.models import City
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
    city_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    def validate(self, attrs):
        city_id = attrs.get('city_id')
        if city_id is not None:
            try:
                city = City.objects.get(pk=city_id)
                attrs['city'] = city
            except City.DoesNotExist:
                raise serializers.ValidationError({'city_id': ["doesn't exist"]})
        return attrs

    class Meta(RegisterSerializer.Meta):
        fields = USER_FIELDS + ("city_id",)
