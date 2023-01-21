from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import validate_email
from django.db import models


# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Group(models.TextChoices):
        PASSPORT = 'Passport'
        INT_PASSPORT = 'International Passport'
        RESIDENT_ID = 'Resident_ID'

    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        max_length=100,
        help_text="Email",
    )
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    photo = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    sex = models.BooleanField(null=True, blank=True)
    doc_type = models.CharField(choices=Group.choices, max_length=30, null=True, blank=True)
    doc_info = models.CharField(max_length=200, null=True, blank=True)
    is_entity = models.BooleanField(default=False)
    activity = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    CV = models.FileField(upload_to=user_directory_path, null=True, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']


class UserCreateCode(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=True, blank=True)
