from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.models import update_last_login
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty, SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from JustDoIT.backends import authenticate
from authentication import utils
from authentication.utils import count_average
from authentication.models import UserCreateCode, ActivityCategory, CustomUser, Review

User = get_user_model()


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityCategory
        fields = ('id', 'description')


class UserCreateSerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'firstname', 'groups',
                  'lastname', 'photo', 'sex', 'region', 'doc_type', 'doc_info',
                  'is_entity', 'activity', 'image', 'CV', 'activities')
        extra_kwargs = {'activities': {'required': False, 'write_only': True}}


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
            try:
                assert data.get('password')
            except AssertionError:
                raise ValidationError('Вы не ввели пароль')
            code.delete()
            if not user.is_active:
                raise ValidationError('Пользователь не активен для восстановления пароля')
            user.set_password(data.get("password"))
            user.save()
        else:
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

class UserProfileSerializer(serializers.ModelSerializer):
    rating = SerializerMethodField()

    class Meta:
        model = User
        # TODO как обозначить обязательные поля?
        # TODO добавить поле Описание фото + загрузить фото +загрузить рюземе (не обязательно);
        fields = ('firstname', 'lastname', 'groups', 'rating', 'phone_number', 'email',
                  'photo', 'password', 'region', 'activities', 'groups',
                  'doc_type', 'doc_info')

    def get_rating(self, obj):
        count_average_ = count_average(obj.reviews.all())
        print(count_average_)
        return count_average_


class ReviewSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(read_only=True)
    user = UserProfileSerializer(write_only=True)

    def create(self, validated_data):
        instance, _ = Review.objects.get_or_create(**validated_data)
        print(instance, _)
        return instance

    class Meta:
        model = Review
        fields = '__all__'
