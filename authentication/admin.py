from django.contrib import admin

# Register your models here.
from authentication.models import CustomUser, UserCreateCode, ActivityCategory, Review

admin.site.register(CustomUser)


admin.site.register(UserCreateCode)
admin.site.register(ActivityCategory)
admin.site.register(Review)
