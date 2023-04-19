from django.db import models


class Chat(models.Model):
    users = models.ManyToManyField('authentication.CustomUser', related_name='chats',
                                   verbose_name='От кого', null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'chat'


class CustomManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('id')
        return queryset


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True, blank=True, related_name='messages',
                             verbose_name='Чат')
    time = models.DateTimeField(auto_now_add=True, verbose_name='Время')
    text = models.CharField(max_length=1000, verbose_name='Текст сообщения')
    owner = models.ForeignKey('authentication.CustomUser', on_delete=models.SET_NULL, related_name='messages',
                              verbose_name='Автор', null=True, blank=True)

    objects = CustomManager()

    class Meta:
        managed = True
        db_table = 'messages'
