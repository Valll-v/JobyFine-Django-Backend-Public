from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.models import CustomUser, ExpImage
from authentication.serializers import ActivitySerializer, ExpImgSerializer

User = get_user_model()


class ShortProfileInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname', 'photo')


class UpdateProfileSerializer(serializers.ModelSerializer):
    images = ExpImgSerializer(many=True, read_only=True)

    def save(self, **kwargs):
        user: CustomUser = super(UpdateProfileSerializer, self).save()
        images = self.initial_data.getlist('images')
        if images is not None:
            user.images.all().delete()
            for img in images:
                ExpImage.objects.create(user=user, image=img)
        return user

    class Meta:
        model = User
        fields = ('email', 'firstname', 'lastname', 'photo', 'sex', 'country', 'region', 'doc_type', 'doc_info',
                  'is_entity', 'activity', 'activities', 'CV', 'images')
        extra_kwargs = {
            'email': {'required': False},
            'firstname': {'required': False},
            'lastname': {'required': False},
        }


class ProfileSerializer(serializers.ModelSerializer):
    activities_info = ActivitySerializer(many=True, read_only=True, source='activities')
    images = ExpImgSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'firstname', 'groups',
                  'lastname', 'photo', 'sex', 'country', 'region', 'doc_type', 'doc_info',
                  'is_entity', 'activity', 'CV', 'activities_info', 'last_seen', 'images', 'balance', 'link')


# class UpdatePhoneSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#
#     def is_valid(self, raise_exception=False):
#         super(UpdatePhoneSerializer, self).is_valid()
#         if User.objects.filter(phone_number=self.initial_data.get('phone_number')):
#             raise ValidationError('This phone number is occupied')
#
#     def save(self, **kwargs):
#         code: PhoneUpdate = super(UpdatePhoneSerializer, self).save(**kwargs)
#         code.gen_code()
#         return code
#
#     class Meta:
#         model = PhoneUpdate
#         fields = ('id', 'user', 'phone_number')
#
#
# class UpdateCodeSerializer(serializers.ModelSerializer):
#
#     def is_valid(self, raise_exception=True):
#         assert hasattr(self, 'initial_data'), (
#             'Cannot call `.is_valid()` as no `data=` keyword argument was '
#             'passed when instantiating the serializer instance.'
#         )
#         user: CustomUser = self.context.get('request').user
#         code: PhoneUpdate = self.instance
#         try:
#             assert self.instance.code == self.initial_data.get('code')
#         except AssertionError:
#             raise ValidationError('Неверный код')
#         else:
#             user.phone_number = code.phone_number
#             user.save()
#             code.delete()
