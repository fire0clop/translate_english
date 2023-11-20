from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Translation, Statys
import g4f
from googletrans import Translator


def ViewForMain(request):
    return render(request, template_name='WordBase/main_page.html')


def mainbase(request):
    return render(request, template_name='WordBase/Base.html')


def group_words(request):
    # Считаем количество объектов модели со статусом 1
    status_1 = Translation.objects.filter(statys__id=1).count()
    # Считаем количество объектов модели со статусом 2
    status_2 = Translation.objects.filter(statys__id=2).count()
    # Считаем количество объектов модели со статусом 3
    status_3 = Translation.objects.filter(statys__id=3).count()

    # Добавляем это количество в контекст для передачи в шаблон
    context = {
        'status_1': status_1,
        'status_2': status_2,
        'status_3': status_3,
    }

    return render(request, 'WordBase/class_base.html', context)


class ListBaseView(ListView):
    template_name = 'WordBase/base_word_list.html'
    model = Translation
    context_object_name = 'translate'

    def get_queryset(self):
        translate = Translation.objects.filter(user=self.request.user).order_by('statys__id')
        return translate


def create_word(request):
    if request.method == 'POST':
        word = request.POST.get('word')
        word = word.capitalize()

        def detect_language_by_alphabet(text):
            cyrillic_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
            latin_letters = 'abcdefghijklmnopqrstuvwxyz'

            cyrillic_count = sum(1 for char in text if char.lower() in cyrillic_letters)
            latin_count = sum(1 for char in text if char.lower() in latin_letters)

            if cyrillic_count > latin_count:
                return 'ru'  # Если кириллических символов больше, считаем текст на русском
            elif latin_count > cyrillic_count:
                return 'en'  # Если латинских символов больше, считаем текст на английском
            else:
                return None  # Если одинако

        detected_language = detect_language_by_alphabet(word)
        translator = Translator()
        # Если введенное написано слово на русском языке
        if detected_language == 'ru':

            # перевод с русского на английский
            result = translator.translate(word, src='ru', dest='en')
            english_word = result.text

            # Создаем объект Translation с передачей request
            translation = Translation(russian_word=word, english_word=english_word, user=request.user)
            translation.save()

        # В остальных случаях понимаем что слово введено на английском языке
        else:
            result = translator.translate(word, src='en', dest='ru')
            russian_word = result.text
            # Создаем объект Translation с передачей request
            translation = Translation(english_word=word, russian_word=russian_word, user=request.user)
            translation.save()
        return redirect('list_base')

    return render(request, 'WordBase/create_word.html')


class DetailBaseView(DetailView):
    template_name = 'WordBase/detail_word.html'
    model = Translation
    context_object_name = 'translate'


class UpdateBaseView(UpdateView):
    template_name = 'WordBase/edit_word.html'
    model = Translation
    fields = 'russian_word', 'english_word'
    success_url = reverse_lazy('list_base')


class ChangeStatusView(View):
    def post(self, request, *args, **kwargs):
        # Получите данные из POST-запроса
        selected_word_ids = request.POST.getlist('selectedWordIds[]', [])
        button_value = int(request.POST.get('buttonValue'))
        new_status = get_object_or_404(Statys, id=button_value)
        for word_id in selected_word_ids:
            word_ob = get_object_or_404(Translation, id=word_id)
            word_ob.statys = new_status
            word_ob.save()

        return HttpResponseRedirect(reverse_lazy('list_base'))


class DeleteSelectedWordsView(View):
    def post(self, request, *args, **kwargs):
        # Получите список ID выбранных слов из POST-запроса
        selected_word_ids = request.POST.getlist('selectedWordIds[]', [])

        # Убедитесь, что список не пустой
        if selected_word_ids:
            try:
                # Удалите выбранные слова из базы данных
                Translation.objects.filter(id__in=selected_word_ids).delete()

                return JsonResponse({'success': 'Selected words deleted successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'No words selected for deletion'})
