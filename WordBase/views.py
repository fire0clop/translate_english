from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView,DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Translation
from googletrans import Translator

def ViewForMain(request):
    return render(request, template_name = 'WordBase/main_page.html')
def mainbase(request):
    return render(request, template_name='WordBase/Base.html')

class ListBaseView(ListView):
    template_name = 'WordBase/base_word_list.html'
    model = Translation
    context_object_name = 'translate'

def create_word(request):
    if request.method == 'POST':
        word =request.POST.get('word')
        translator = Translator()
        lang = translator.detect(word)
        print(lang.lang)
        if lang.lang == 'ru':
            translation = translator.translate(word, src='ru', dest='es')
            spanish_word = translation.text
            translation = Translation(russian_word=word, spanish_word=spanish_word)
            translation.save()
        else:
            translation = translator.translate(word, src='es', dest='ru')
            russian_word = translation.text
            translation = Translation(spanish_word=word, russian_word=russian_word)
            translation.save()
        return redirect('list_base')


    return render(request, 'WordBase/create_word.html')
class DetailBaseView(DetailView):
    template_name = 'WordBase/detail_word.html'
    model = Translation
    context_object_name = 'translate'
class DeleteBaseView(DeleteView):
    template_name = 'WordBase/delete_word.html'
    model = Translation
    success_url = reverse_lazy('list_base')
class UpdateBaseView(UpdateView):
    template_name = 'WordBase/create_word.html'
    model = Translation
    fields = 'russian_word', 'spanish_word'
    success_url = reverse_lazy('list_base')