from django.db import models
from django.utils.translation import gettext_lazy as _
from googletrans import Translator

class Translation(models.Model):
    russian_word = models.CharField(_('Russian Word'), max_length=100)
    spanish_word = models.CharField(_('Spanish Word'), max_length=100)
    def __str__(self):
        return self.russian_word

    class Meta:
        verbose_name = _('Translation')
        verbose_name_plural = _('Translations')
