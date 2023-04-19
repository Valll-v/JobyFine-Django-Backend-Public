from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.db.models import Q
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from JustDoIT import settings
from JustDoIT.backends import authenticate
from authentication.models import UserCreateCode, ActivityCategory, SubCategory, ExpImage

User = get_user_model()


class SubActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'description')


class ActivitySerializer(serializers.ModelSerializer):
    subcategories = SubActivitySerializer(many=True, read_only=True)

    class Meta:
        model = ActivityCategory
        fields = ('id', 'description', 'photo', 'subcategories')


class ExpImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpImage
        fields = ('image', )


class UserCreateSerializer(serializers.ModelSerializer):
    activities_info = ActivitySerializer(many=True, read_only=True, source='activities')
    password = serializers.CharField(write_only=True, required=True)
    images = ExpImgSerializer(many=True, read_only=True)

    def is_valid(self, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )
        data = self.initial_data
        if self.initial_data.get('phone_number') and self.initial_data.get('email'):
            user = User.objects.filter(Q(email=data.get('email')) | Q(phone_number=data.get('phone_number'))).first()
            if user and not user.is_active:
                user.delete()
        return super(UserCreateSerializer, self).is_valid(raise_exception)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if user:
            images = self.initial_data.getlist('images')
            print(images)
            if images:
                for img in images:
                    ExpImage.objects.create(user=user, image=img)
        return user

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'firstname', 'groups',
                  'lastname', 'photo', 'sex', 'region', 'country', 'doc_type', 'doc_info',
                  'is_entity', 'activity', 'CV', 'activities', 'activities_info', 'images')
        extra_kwargs = {'activities': {'required': False, 'write_only': True}}


class ProfileSerializer(serializers.ModelSerializer):
    activities_info = ActivitySerializer(many=True, read_only=True, source='activities')
    images = ExpImgSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'firstname', 'groups',
                  'lastname', 'photo', 'sex', 'region', 'country', 'doc_type', 'doc_info',
                  'is_entity', 'activity', 'CV', 'activities_info', 'last_seen', 'images', 'balance')


class UpdatePasswordSerializer(serializers.ModelSerializer):

    def is_valid(self, raise_exception=False):
        data = self.initial_data
        user = data.get(User.USERNAME_FIELD)
        try:
            user = User.objects.get_by_natural_key(user)
        except User.DoesNotExist:
            raise ValidationError('Пользователь под данным номером не обнаружен')
        return user


class CodeSerializer(serializers.ModelSerializer):

    def is_valid(self, raise_exception=True):
        data = self.initial_data
        user = data.get(User.USERNAME_FIELD)
        try:
            user = User.objects.get_by_natural_key(user)
            code = UserCreateCode.objects.get(user=user)
            assert code.code == data.get('code')
        except User.DoesNotExist:
            raise ValidationError('Пользователь под данным номером не обнаружен')
        except UserCreateCode.DoesNotExist:
            raise ValidationError('Невозможно подтвердить код')
        except AssertionError:
            raise ValidationError('Неверный код')
        if hasattr(self, 'update_passwd'):
            user.update_pass = True
            user.save()
        else:
            ref = self.initial_data.get('ref_code')
            if ref:
                father_user = User.objects.filter(pk=ref).first()
                if father_user:
                    father_user.balance += settings.COIN
                    father_user.save()
            code.delete()
            user.is_active = True
            user.save()
        return user

    class Meta:
        model = UserCreateCode


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        self.user = authenticate(attrs[self.username_field], attrs["password"])

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        refresh = self.get_token(self.user)

        data = {"refresh": str(refresh), "access": str(refresh.access_token)}

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
