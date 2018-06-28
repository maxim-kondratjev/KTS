from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.text
