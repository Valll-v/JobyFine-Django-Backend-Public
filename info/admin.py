from django import forms
from django.contrib import admin
# Register your models here.
from info.models import ProjectInfo, Question


class QuestionAdminForm(forms.ModelForm):

    class Meta:
        model = Question
        widgets = {
            'answer': forms.Textarea(),
        }
        fields = ('question', 'answer')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    form = QuestionAdminForm


class InfoAdminForm(forms.ModelForm):

    class Meta:
        model = ProjectInfo
        widgets = {
            'about': forms.Textarea(),
            'confidence': forms.FileInput(),
            'agreement': forms.FileInput(),
        }
        fields = ('about', 'confidence', 'agreement')


@admin.register(ProjectInfo)
class ProjectInfoAdmin(admin.ModelAdmin):
    list_display = ('about', 'confidence', 'agreement')
    form = InfoAdminForm

    def has_add_permission(self, request):
        return not ProjectInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
