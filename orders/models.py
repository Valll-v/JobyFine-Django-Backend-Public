from django.db import models


def image_user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/order_{1}/{2}'.format(instance.order.owner.id, instance.order.id, filename)


# Create your models here.
class Order(models.Model):
    owner = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, null=True, verbose_name='Создатель',
                              related_name='orders')
    name = models.CharField(max_length=1024, verbose_name='Название вашей задачи')
    description = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Описание задачи')

    created_date = models.DateTimeField(auto_now_add=True)
    subcategory = models.ForeignKey('authentication.SubCategory', on_delete=models.CASCADE,
                                    verbose_name='Подкатегория', related_name='orders')
    date_start = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата окончания')
    price_from = models.IntegerField(verbose_name='Бюджет от')
    price_to = models.IntegerField(verbose_name='Бюджет до')
    region = models.CharField(max_length=1024, verbose_name='Регион')

    class Meta:
        managed = True
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


class OrderFile(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=image_user_directory_path, null=True, blank=True, verbose_name='Аватарка')
