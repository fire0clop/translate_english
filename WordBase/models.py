from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class Statys(models.Model):
    name = models.CharField(max_length=50)
class Translation(models.Model):
    russian_word = models.CharField(_('Russian Word'), max_length=100)
    spanish_word = models.CharField(_('Spanish Word'), max_length=100)
    statys = models.ForeignKey(Statys, default=1, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.russian_word

    class Meta:
        verbose_name = _('Translation')
        verbose_name_plural = _('Translations')

    def save(self, *args, **kwargs):
        # Проверяем, есть ли request в kwargs
        request = kwargs.pop('request', None)

        # Если request есть и пользователь залогинен, устанавливаем user
        if request and request.user.is_authenticated:
            self.user = request.user

        super(Translation, self).save(*args, **kwargs)
