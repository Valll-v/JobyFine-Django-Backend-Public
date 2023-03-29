from django.contrib.auth import get_user_model
from rest_framework import serializers
from authentication.serializers import ActivitySerializer

User = get_user_model()


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'firstname', 'lastname', 'photo', 'sex', 'region', 'doc_type', 'doc_info',
                  'is_entity', 'activity', 'activities', 'image', 'CV')
        extra_kwargs = {
            'email': {'required': False},
            'firstname': {'required': False},
            'lastname': {'required': False},
        }


class ProfileSerializer(serializers.ModelSerializer):
    activities_info = ActivitySerializer(many=True, read_only=True, source='activities')

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'firstname', 'groups',
                  'lastname', 'photo', 'sex', 'region', 'doc_type', 'doc_info',
                  'is_entity', 'activity', 'image', 'CV', 'activities_info', 'last_seen')
