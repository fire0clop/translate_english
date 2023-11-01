from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Translation, Statys
from translate import Translator
import g4f


def ViewForMain(request):
    return render(request, template_name='WordBase/main_page.html')


def mainbase(request):
    return render(request, template_name='WordBase/Base.html')


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
                return 'en'  # Если латинских символов больше, считаем текст на испанском
            else:
                return None  # Если одинако

        detected_language = detect_language_by_alphabet(word)

        # Если введенное написано слово на русском языке
        if detected_language == 'ru':
            content = f"Переведи слово: '{word}' на английский язык. в ответе пришли только само одно слово! слово-перевод! и обязательно больше никаких слов и символов в ответе не пиши"
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": content}],
                stream=True,
            )

            translate_word = ''
            for message in response:
                translate_word += message
            print(translate_word)

            # Создаем объект Translation с передачей request
            translation = Translation(russian_word=word, english_word=translate_word, user=request.user)
            translation.save()

        # В остальных случаях понимаем что слово введено на испанском языке
        else:
            content = f"Переведи слово: '{word}' на русский язык. в ответе пришли только само одно слово! слово-перевод! и обязательно больше никаких слов и символов в ответе не пиши"
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": content}],
                stream=True,
            )

            translate_word = ''
            for message in response:
                translate_word += message
            print(translate_word)
            # Создаем объект Translation с передачей request
            translation = Translation(english_word=word, russian_word=translate_word, user=request.user)
            translation.save()
        return redirect('list_base')

    return render(request, 'WordBase/create_word.html')


class DetailBaseView(DetailView):
    template_name = 'WordBase/detail_word.html'
    model = Translation
    context_object_name = 'translate'


class UpdateBaseView(UpdateView):
    template_name = 'WordBase/create_word.html'
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
