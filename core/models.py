from django.contrib.auth.models import User, AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(AbstractUser):
    avatar = models.FileField(blank=True, null=True, default=None, verbose_name='Аватар')

    objects = UserManager()

    class Meta:
        db_table = 'profiles'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')


class Message(models.Model):
    author = models.ForeignKey(Profile, verbose_name='Автор', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст', blank=True, null=True, default='')
    date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    file = models.FileField(verbose_name= 'Прикрепленный файл', blank=True, default=None, null=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.text



