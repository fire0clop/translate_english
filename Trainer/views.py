from django.http import JsonResponse
from django.shortcuts import render
from .backend import random_choise, generate_rus_word, generate_eng_word
from WordBase.models import Translation
import random


# Create your views here.
def trainer_choise(request):
    return render(request, 'Trainer/trainer_choise.html')


def training(request):
    es_user = request.user
    options = ['en', 'ru']
    translations = Translation.objects.filter(user=es_user, statys=2)
    if translations:
        elected_value = random.choice(options)
        if elected_value == 'en':
            out_obj = random_choise(translations)
            bad_word = generate_rus_word()
        else:
            out_obj = random_choise(translations)
            bad_word = generate_eng_word()
        return render(request, 'Trainer/first_training.html',
                      {'word': out_obj, 'bad_word': bad_word, 'elected_value': elected_value})
    else:
        return render(request, 'Trainer/Noword.html')


def new_correct(request):
    if request.method == 'POST':
        word = request.POST.get('word')

        # Найдите запись Translation по слову (или использовать другой способ поиска)
        translation = Translation.objects.get(russian_word=word)

        # Увеличьте поле progress на 1 и сохраните изменения
        if translation.progress < 20:
            translation.progress += 1
            translation.save()
        else:
            pass

        return JsonResponse({'reload_page': True})


def new_wrong(request):
    if request.method == 'POST':
        word = request.POST.get('word')

        # Найдите запись Translation по слову (или использовать другой способ поиска)
        translation = Translation.objects.get(russian_word=word)

        # Увеличьте поле progress на 1 и сохраните изменения
        if translation.progress >= 2:
            translation.progress -= 2
            translation.save()
        elif translation.progress == 1:
            translation.progress -= 1
            translation.save()
        else:
            pass

        return JsonResponse({'reload_page': True})
