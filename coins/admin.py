from PIL import Image
from django.contrib import admin


# Register your models here.
from django.contrib.admin import forms

from coins.models import Level
from django import forms


@admin.register(Level)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'must_coins', 'image', 'bw_image')
