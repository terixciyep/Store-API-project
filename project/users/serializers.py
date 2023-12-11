from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

from users.models import UserModel


class UserModelSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return UserModel.object.create_user(email=validated_data['email'], password=validated_data['password'])

    class Meta:
        model = UserModel
        fields = '__all__'