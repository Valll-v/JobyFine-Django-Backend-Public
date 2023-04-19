from django.contrib import admin


# Register your models here.
from orders.models import Order


@admin.register(Order)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_date', 'description')
