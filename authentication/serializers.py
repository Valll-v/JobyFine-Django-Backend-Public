from rest_framework import serializers

from authentication.models import CustomUser


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
