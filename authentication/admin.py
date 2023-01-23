from django.contrib import admin

# Register your models here.
from authentication.models import CustomUser, UserCreateCode

admin.site.register(CustomUser)


admin.site.register(UserCreateCode)