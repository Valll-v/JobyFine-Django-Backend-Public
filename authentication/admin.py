from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from authentication.models import ActivityCategory, SubCategory


User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'phone_number', 'firstname', 'lastname', 'photo', 'last_seen')
    list_filter = ()
    ordering = ()
    fieldsets = (
        (None, {'fields': (
            'phone_number',
            'firstname',
            'lastname',
            'photo'
        )}),
    )
    search_fields = ('phone_number', 'firstname', 'lastname')

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(User, CustomUserAdmin)


@admin.register(ActivityCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('description', 'photo', 'order_int')


@admin.register(SubCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'description')

