from django.db import models


# Create your models here.
class Review(models.Model):
    reviewer = models.ForeignKey('authentication.CustomUser', on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='sent_reviews', verbose_name='От кого')
    receiver = models.ForeignKey('authentication.CustomUser', related_name='reviews', on_delete=models.CASCADE,
                                 verbose_name='На кого')
    message = models.CharField(max_length=10000, verbose_name='Отзыв')
    mark = models.IntegerField(verbose_name='Оценка')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')

    class Meta:
        managed = True
        db_table = 'reviews'
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
