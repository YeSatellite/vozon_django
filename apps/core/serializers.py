from rest_framework.serializers import ModelSerializer


class UserOwnerMixin(object):
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super(ModelSerializer).create(validated_data)

