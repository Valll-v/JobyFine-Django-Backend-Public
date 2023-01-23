from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.apps import apps
from django.contrib.auth.models import PermissionsMixin, UserManager, Group
from django.core.validators import validate_email
from django.db import models


# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        print("aboba")
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def _create_user(self, phone_number, email, password, **extra_fields):
        groups = extra_fields.pop('groups', [])
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        user.groups.set(groups)
        return user

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, email, password, **extra_fields)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Docs(models.TextChoices):
        PASSPORT = 'Passport'
        INT_PASSPORT = 'International Passport'
        RESIDENT_ID = 'Resident_ID'

    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        max_length=100,
        help_text="Email",
    )
    is_active = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    photo = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    sex = models.BooleanField(null=True, blank=True)
    doc_type = models.CharField(choices=Docs.choices, max_length=30, null=True, blank=True)
    doc_info = models.CharField(max_length=200, null=True, blank=True)
    is_entity = models.BooleanField(default=False)
    activity = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    CV = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    @property
    def is_authenticated(self):
        return self.is_active

    groups = models.ManyToManyField(
        Group,
        blank=False,
        related_name="user_set",
        related_query_name="user",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'firstname', 'lastname', 'groups']

    def __str__(self):
        return str(self.phone_number)


class UserCreateCode(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=True, blank=True)
