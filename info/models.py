from django.db import models


def project_info_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'project_info/{0}'.format(filename)


# Create your models here.
class ProjectInfo(models.Model):
    about = models.CharField(max_length=1000, verbose_name='О проекте', null=True)
    confidence = models.FileField(upload_to=project_info_path, verbose_name='Пользовательское соглашение', null=True)
    agreement = models.FileField(upload_to=project_info_path, verbose_name='Согласие на обработку персональных данных',
                                 null=True)

    class Meta:
        db_table = 'project_info'
        verbose_name = 'О проекте'
        verbose_name_plural = 'О проекте'


class Question(models.Model):
    question = models.CharField(max_length=100, verbose_name='Вопрос')
    answer = models.CharField(max_length=300, verbose_name='Ответ')

    class Meta:
        db_table = 'questions'
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопрос - Ответ'
