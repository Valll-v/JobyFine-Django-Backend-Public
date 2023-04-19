from django.db import models


def level_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'project_info/levels/{0}'.format(filename)

#
# class LevelManager(models.Manager):
#
#     def get_queryset(self):
#         return


# Create your models here.
class Level(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    must_coins = models.IntegerField(verbose_name='Нужно баллов')
    image = models.FileField(upload_to=level_path, verbose_name='Изображение')
    bw_image = models.FileField(upload_to=level_path, verbose_name='Черно-Белое изображение', null=True, blank=True)
