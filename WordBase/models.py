from django.db import models
from django.utils.translation import gettext_lazy as _
from googletrans import Translator

class Translation(models.Model):
    russian_word = models.CharField(_('Russian Word'), max_length=100)
    spanish_word = models.CharField(_('Spanish Word'), max_length=100)

    def save(self, *args, **kwargs):
        if not self.id:  # Если запись только создается, то переводим слово
            translator = Translator()
            translation = translator.translate(self.russian_word, src='ru', dest='es')
            self.spanish_word = translation.text
        super().save(*args, **kwargs)

    def __str__(self):
        return self.russian_word

    class Meta:
        verbose_name = _('Translation')
        verbose_name_plural = _('Translations')
